# components/forms.py

import streamlit as st
import pandas as pd
import numpy as np
from config.settings import SUBJECTS, SEMESTER_1_SUBJECTS, SEMESTER_2_SUBJECTS, ACADEMIC_YEAR
from database.grades import save_grade, load_grades
from database.users import create_user, get_all_users, delete_user
from utils.calculations import calculate_average, calculate_grade
from utils.helpers import can_take_semester_2

def add_grade_form(conn):
    st.title("Thêm điểm sinh viên")
    
    semester = st.radio("Chọn học kỳ", [1, 2], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        mssv = st.text_input("MSSV *")
        student_name = st.text_input("Họ tên *")
        class_name = st.text_input("Lớp")
    
    can_sem2 = True
    if semester == 2 and mssv:
        can_sem2, message = can_take_semester_2(conn, mssv)
        if can_sem2:
            st.success(f"{message}")
        else:
            st.error(f"{message}")
    
    st.subheader(f"Điểm các môn - Học kỳ {semester}")
    
    current_subjects = SEMESTER_1_SUBJECTS if semester == 1 else SEMESTER_2_SUBJECTS
    
    subject_scores = {}
    cols = st.columns(3)
    for i, key in enumerate(current_subjects):
        info = SUBJECTS[key]
        with cols[i % 3]:
            label = info['name']
            if not info['counts_gpa']:
                label += " (Không tính GPA)"
            if info.get('mandatory'):
                label += " *"
            subject_scores[key] = st.number_input(label, 0.0, 10.0, 0.0, key=f"add_{key}")
    
    st.info(f"Năm học: **{ACADEMIC_YEAR}** (cố định)")
    
    if st.button("Thêm điểm", type="primary", disabled=(semester == 2 and not can_sem2)):
        if mssv and student_name:
            scores_for_avg = {k: v for k, v in subject_scores.items() 
                           if SUBJECTS[k]['counts_gpa'] and v > 0}
            diem_tb = round(np.mean(list(scores_for_avg.values())), 2) if scores_for_avg else 0.0
            xep_loai = calculate_grade(diem_tb)
            
            all_scores = {k: None for k in SUBJECTS.keys()}
            all_scores.update(subject_scores)
            
            params = (
                mssv, student_name, class_name, int(semester),
                float(all_scores['triet']) if all_scores['triet'] is not None else None,
                float(all_scores['giai_tich_1']) if all_scores['giai_tich_1'] is not None else None,
                float(all_scores['giai_tich_2']) if all_scores['giai_tich_2'] is not None else None,
                float(all_scores['tieng_an_do_1']) if all_scores['tieng_an_do_1'] is not None else None,
                float(all_scores['tieng_an_do_2']) if all_scores['tieng_an_do_2'] is not None else None,
                float(all_scores['gdtc']) if all_scores['gdtc'] is not None else None,
                float(all_scores['thvp']) if all_scores['thvp'] is not None else None,
                float(all_scores['tvth']) if all_scores['tvth'] is not None else None,
                float(all_scores['phap_luat']) if all_scores['phap_luat'] is not None else None,
                float(all_scores['logic']) if all_scores['logic'] is not None else None,
                float(diem_tb), xep_loai, int(ACADEMIC_YEAR)
            )
            ok, err = save_grade(conn, params)
            if ok:
                st.success(f"Đã thêm điểm cho {student_name} - ĐTB: {diem_tb} - Xếp loại: {xep_loai}")
            else:
                st.error(f"Lỗi khi lưu vào DB: {err}")
        else:
            st.error("Vui lòng nhập MSSV và Họ tên!")

def import_data(conn):
    st.title("Import dữ liệu")
    
    option = st.radio(
        "Chọn loại dữ liệu cần nhập:",
        ["Học kỳ 1", "Học kỳ 2", "Cả hai kỳ"],
        horizontal=True
    )
    
    if option == "Học kỳ 1":
        st.info("Định dạng CSV: mssv, student_name, class_name, semester (=1), triet, giai_tich_1, tieng_an_do_1, gdtc, thvp")
    elif option == "Học kỳ 2":
        st.info("Định dạng CSV: mssv, student_name, class_name, semester (=2), giai_tich_2, tieng_an_do_2, tvth, phap_luat, logic")
    else:
        st.info("CSV cho cả hai kỳ: mssv, student_name, class_name, semester, điểm theo từng kỳ")
    
    uploaded_file = st.file_uploader("Chọn file CSV", type=['csv'])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Xem trước dữ liệu:")
            st.dataframe(df.head(10))
            
            if st.button("Import vào database"):
                c = conn.cursor()
                
                for key in SUBJECTS.keys():
                    if key not in df.columns:
                        df[key] = np.nan
                    else:
                        df[key] = pd.to_numeric(df[key], errors='coerce')
                
                count_inserted = 0
                
                for _, row in df.iterrows():
                    semester = int(row.get("semester", 1))
                    
                    if option == "Học kỳ 1" and semester != 1:
                        continue
                    if option == "Học kỳ 2" and semester != 2:
                        continue
                    
                    diem_tb = calculate_average(row)
                    xep_loai = calculate_grade(diem_tb)
                    
                    params = (
                        row.get('mssv', ''), row.get('student_name', ''), row.get('class_name', ''),
                        semester,
                        None if pd.isna(row['triet']) else float(row['triet']),
                        None if pd.isna(row['giai_tich_1']) else float(row['giai_tich_1']),
                        None if pd.isna(row['giai_tich_2']) else float(row['giai_tich_2']),
                        None if pd.isna(row['tieng_an_do_1']) else float(row['tieng_an_do_1']),
                        None if pd.isna(row['tieng_an_do_2']) else float(row['tieng_an_do_2']),
                        None if pd.isna(row['gdtc']) else float(row['gdtc']),
                        None if pd.isna(row['thvp']) else float(row['thvp']),
                        None if pd.isna(row['tvth']) else float(row['tvth']),
                        None if pd.isna(row['phap_luat']) else float(row['phap_luat']),
                        None if pd.isna(row['logic']) else float(row['logic']),
                        float(diem_tb), xep_loai, int(ACADEMIC_YEAR)
                    )
                    
                    try:
                        c.execute('''INSERT INTO grades (mssv, student_name, class_name, semester,
                                     triet, giai_tich_1, giai_tich_2, tieng_an_do_1, tieng_an_do_2,
                                     gdtc, thvp, tvth, phap_luat, logic,
                                     diem_tb, xep_loai, academic_year)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', params)
                        count_inserted += 1
                    except Exception as e:
                        print("Lỗi khi insert:", e)
                
                conn.commit()
                st.success(f"Đã import {count_inserted} bản ghi thành công!")
                st.rerun()
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")

def export_data(df):
    st.title("Export dữ liệu")
    
    if df.empty:
        st.warning("Không có dữ liệu để export.")
        return
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("Tải file CSV", csv, "student_grades.csv", "text/csv")

def clean_data_page(conn, df):
    st.title("Làm sạch & chuẩn hoá dữ liệu học tập")

    st.subheader("Phân tích dữ liệu hiện tại")

    if df.empty:
        st.warning("Chưa có dữ liệu để phân tích.")
        return

    # Trùng MSSV + học kỳ + năm học
    duplicate_count = int(df.duplicated(subset=["mssv", "semester", "academic_year"], keep="first").sum())

    # MSSV có nhiều tên khác nhau
    name_conflict_count = int((df.groupby("mssv")["student_name"].nunique() > 1).sum())

    col1, col2 = st.columns(2)
    with col1:
        if duplicate_count > 0 or name_conflict_count > 0:
            st.error(f"- {duplicate_count} bản ghi trùng (MSSV + Học kỳ + Năm học)\n- {name_conflict_count} MSSV có nhiều tên khác nhau")
        else:
            st.success("Không có bản ghi trùng và MSSV có nhiều tên khác nhau")

    st.divider()

    st.subheader("Các bước làm sạch sẽ thực hiện")
    st.write("- Loại bỏ bản ghi trùng **MSSV + Học kỳ + Năm học**")
    st.write("- Xử lý MSSV có nhiều tên khác nhau (giữ bản ghi đầu tiên)")
    st.write("- Tính lại điểm trung bình và xếp loại")

    if st.button(
        "Làm sạch dữ liệu",
        type="primary",
        disabled=(duplicate_count == 0 and name_conflict_count == 0)
    ):
        try:
            from database.clean import clean_data

            removed_duplicates, removed_name_conflict, _ = clean_data(conn)

            st.success(
                "Hoàn thành làm sạch dữ liệu!\n\n"
                f"- Đã loại bỏ **{removed_duplicates}** bản ghi trùng\n"
                f"- Đã loại bỏ **{removed_name_conflict}** bản ghi do MSSV có nhiều tên"
            )
            st.rerun()

        except Exception as e:
            st.error(f"Lỗi khi làm sạch dữ liệu: {e}")

def manage_users(conn):
    st.title("Quản lý tài khoản")
    
    tab_list, tab_create = st.tabs(["Danh sách", "Thêm mới"])
    
    with tab_list:
        users_df = get_all_users(conn)
        st.dataframe(users_df, use_container_width=True)
        
        deletable = users_df[users_df["username"] != "admin"]
        
        if not deletable.empty:
            user_id = st.selectbox("Chọn user để xóa", deletable["id"].tolist())
            if st.button("Xóa user", type="primary"):
                with st.spinner("Đang xóa..."):
                    delete_user(conn, user_id)
                st.success("Đã xóa tài khoản!")
                st.rerun()
    
    with tab_create:
        st.subheader("Thêm tài khoản mới")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        fullname = st.text_input("Họ tên")
        role = st.selectbox("Vai trò", ["student", "teacher"])
        student_id = st.text_input("MSSV") if role == "student" else None
        
        if st.button("Tạo tài khoản", type="primary"):
            if not username or not password or not fullname:
                st.error("Vui lòng điền đầy đủ thông tin!")
                return
            
            with st.spinner("Đang tạo..."):
                created = create_user(conn, username, password, fullname, role, student_id)
            
            if created:
                st.success("Tạo tài khoản thành công!")
                st.rerun()
            else:
                st.error("Username đã tồn tại!")



