# components/tables.py
import datetime
from datetime import datetime, date, timedelta
import streamlit as st
import pandas as pd
from utils.calculations import calculate_grade, get_ranking_by_semester
from database.grades import delete_grade, delete_grades_batch
from config.settings import SUBJECTS, SEMESTER_1_SUBJECTS, SEMESTER_2_SUBJECTS, ACADEMIC_YEAR

def show_ranking(df):
    st.title("Xếp hạng theo điểm GPA")
    
    if df.empty:
        st.warning("Chưa có dữ liệu để xếp hạng.")
        return
    
    semester_option = st.radio(
        "Chọn học kỳ",
        ["Tổng hợp (cả 2 kỳ)", "Học kỳ 1", "Học kỳ 2"],
        horizontal=True
    )
    
    if semester_option == "Học kỳ 1":
        ranking_df = get_ranking_by_semester(df, semester=1)
        if ranking_df.empty:
            st.info("Không có dữ liệu điểm Học kỳ 1.")
            return
        display_cols = ['xep_hang', 'mssv', 'student_name', 'class_name', 'diem_tb', 'xep_loai']
    elif semester_option == "Học kỳ 2":
        ranking_df = get_ranking_by_semester(df, semester=2)
        if ranking_df.empty:
            st.info("Không có dữ liệu điểm Học kỳ 2.")
            return
        display_cols = ['xep_hang', 'mssv', 'student_name', 'class_name', 'diem_tb', 'xep_loai']
    else:
        ranking_df = get_ranking_by_semester(df, semester='all')
        if ranking_df.empty:
            st.info("Chưa có sinh viên nào hoàn thành đủ cả 2 học kỳ.")
            return
        display_cols = ['xep_hang', 'mssv', 'student_name', 'class_name', 'diem_tb_hk1', 'diem_tb_hk2', 'diem_tb', 'xep_loai']
    
    # Top 3
    st.subheader("Top 3 sinh viên xuất sắc")
    top3 = ranking_df.head(3)
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    for i, (_, row) in enumerate(top3.iterrows()):
        if i < 3:
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
                    <h1>{medals[i]}</h1>
                    <h3>{row['student_name']}</h3>
                    <p><strong>MSSV:</strong> {row['mssv']}</p>
                    <p><strong>Điểm TB:</strong> {row['diem_tb']:.2f}</p>
                    <p><strong>Xếp loại:</strong> {row['xep_loai']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("Bảng xếp hạng đầy đủ")
    
    # Bộ lọc
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("Tìm kiếm (MSSV/Tên)", key="ranking_search")
    with col2:
        xep_loai_filter = st.selectbox("Lọc theo xếp loại", 
                                       ['Tất cả'] + list(ranking_df['xep_loai'].dropna().unique()))
    
    filtered_df = ranking_df.copy()
    if search:
        filtered_df = filtered_df[
            filtered_df['mssv'].astype(str).str.contains(search, case=False, na=False) |
            filtered_df['student_name'].str.contains(search, case=False, na=False)
        ]
    if xep_loai_filter != 'Tất cả':
        filtered_df = filtered_df[filtered_df['xep_loai'] == xep_loai_filter]
    
    display_df = filtered_df[display_cols].copy()
    if semester_option == "Tổng hợp (cả 2 kỳ)":
        display_df.columns = ['Xếp hạng', 'MSSV', 'Họ tên', 'Lớp', 'ĐTB HK1', 'ĐTB HK2', 'Điểm TB', 'Xếp loại']
    else:
        display_df.columns = ['Xếp hạng', 'MSSV', 'Họ tên', 'Lớp', 'Điểm TB', 'Xếp loại']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Thống kê
    st.subheader("Thống kê xếp hạng")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tổng số SV", len(ranking_df))
    with col2:
        st.metric("Điểm TB cao nhất", f"{ranking_df['diem_tb'].max():.2f}")
    with col3:
        st.metric("Điểm TB thấp nhất", f"{ranking_df['diem_tb'].min():.2f}")
    with col4:
        excellent_count = len(ranking_df[ranking_df['xep_loai'].isin(['Giỏi', 'Xuất sắc'])])
        st.metric("Số SV Giỏi/Xuất sắc", excellent_count)

def manage_grades_new(conn, df):
    st.title("Quản lý điểm sinh viên")

    if df.empty:
        st.warning("Chưa có dữ liệu điểm.")
        return

    semester_filter = st.radio(
        "Chọn học kỳ hiển thị",
        ['Tất cả từng kỳ', 'Học kỳ 1', 'Học kỳ 2', 'Tổng hợp'],
        horizontal=True
    )

    if semester_filter == 'Học kỳ 1':
        filtered_df = df[df['semester'] == 1].copy()
    elif semester_filter == 'Học kỳ 2':
        filtered_df = df[df['semester'] == 2].copy()
    elif semester_filter == 'Tổng hợp':
        combined_rows = []
        for mssv, group in df.groupby('mssv'):
            if set(group['semester']) == {1, 2}:
                sem1 = group[group['semester'] == 1].iloc[0]
                sem2 = group[group['semester'] == 2].iloc[0]
                dtb = round((sem1['diem_tb'] + sem2['diem_tb']) / 2, 2)
                combined_rows.append({
                    'mssv': mssv,
                    'student_name': sem1['student_name'],
                    'class_name': sem1['class_name'],
                    'diem_tb_hk1': sem1['diem_tb'],
                    'diem_tb_hk2': sem2['diem_tb'],
                    'diem_tb': dtb,
                    'xep_loai': calculate_grade(dtb)
                })
        filtered_df = pd.DataFrame(combined_rows)
    else:
        filtered_df = df.copy()

    if not filtered_df.empty:
        if semester_filter == 'Tổng hợp':
            display_df = filtered_df[['mssv', 'student_name', 'class_name', 'diem_tb_hk1', 'diem_tb_hk2', 'diem_tb', 'xep_loai']]
            display_df.columns = ['MSSV', 'Họ tên', 'Lớp', 'ĐTB HK1', 'ĐTB HK2', 'Điểm TB', 'Xếp loại']
        else:
            display_df = filtered_df[['mssv', 'student_name', 'class_name', 'semester', 'diem_tb', 'xep_loai']]
            display_df.columns = ['MSSV', 'Họ tên', 'Lớp', 'Học kỳ', 'Điểm TB', 'Xếp loại']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.caption(f"Tổng số: {len(display_df)} bản ghi")
    else:
        st.info("Không có dữ liệu phù hợp.")

    st.divider()

    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("Tìm kiếm sinh viên (MSSV hoặc Tên)")
    with col2:
        show_delete = st.checkbox("Hiển thị chức năng Xóa điểm", value=True)

    if search_term:
        search_results = df[
            df['mssv'].astype(str).str.contains(search_term, case=False, na=False) |
            df['student_name'].str.contains(search_term, case=False, na=False)
        ]
        if not search_results.empty:
            st.success(f"Tìm thấy {len(search_results)} bản ghi")
            result_df = search_results[['mssv', 'student_name', 'class_name', 'semester', 'diem_tb', 'xep_loai']]
            result_df.columns = ['MSSV', 'Họ tên', 'Lớp', 'Học kỳ', 'Điểm TB', 'Xếp loại']
            st.dataframe(result_df, use_container_width=True, hide_index=True)

            st.divider()
            
            # === PHẦN SỬA ĐIỂM ===
            st.subheader("Sửa điểm sinh viên")
            
            unique_students = search_results['mssv'].unique().tolist()
            selected_mssv = st.selectbox("Chọn sinh viên để sửa điểm", unique_students)
            
            if selected_mssv:
                student_data = df[df['mssv'] == selected_mssv]
                student_name = student_data.iloc[0]['student_name']
                class_name = student_data.iloc[0]['class_name'] or ''
                
                st.info(f"**Sinh viên:** {student_name} | **MSSV:** {selected_mssv} | **Lớp:** {class_name}")
                
                col_hk1, col_hk2 = st.columns(2)
                
                with col_hk1:
                    st.markdown("### Học kỳ 1")
                    sem1_data = student_data[student_data['semester'] == 1]
                    sem1_scores = {}
                    
                    if not sem1_data.empty:
                        row = sem1_data.iloc[0]
                        for key in SEMESTER_1_SUBJECTS:
                            current_val = row.get(key)
                            current_val = float(current_val) if pd.notna(current_val) else 0.0
                            sem1_scores[key] = st.number_input(
                                SUBJECTS[key]['name'],
                                0.0, 10.0, current_val,
                                key=f"edit_sem1_{key}"
                            )
                    else:
                        st.warning("Chưa có điểm HK1")
                        for key in SEMESTER_1_SUBJECTS:
                            sem1_scores[key] = st.number_input(
                                SUBJECTS[key]['name'],
                                0.0, 10.0, 0.0,
                                key=f"edit_sem1_{key}",
                                disabled=True
                            )
                
                with col_hk2:
                    st.markdown("### Học kỳ 2")
                    sem2_data = student_data[student_data['semester'] == 2]
                    sem2_scores = {}
                    
                    if not sem2_data.empty:
                        row = sem2_data.iloc[0]
                        for key in SEMESTER_2_SUBJECTS:
                            current_val = row.get(key)
                            current_val = float(current_val) if pd.notna(current_val) else 0.0
                            sem2_scores[key] = st.number_input(
                                SUBJECTS[key]['name'],
                                0.0, 10.0, current_val,
                                key=f"edit_sem2_{key}"
                            )
                    else:
                        st.warning("Chưa có điểm HK2 (Sinh viên chưa học)")
                        for key in SEMESTER_2_SUBJECTS:
                            sem2_scores[key] = st.number_input(
                                SUBJECTS[key]['name'],
                                0.0, 10.0, 0.0,
                                key=f"edit_sem2_{key}",
                                disabled=True
                            )
                
                # Nút lưu
                if st.button("Lưu thay đổi", type="primary"):
                    c = conn.cursor()
                    
                    # Cập nhật HK1 nếu có
                    if not sem1_data.empty:
                        sem1_id = sem1_data.iloc[0]['id']
                        scores_for_avg = {k: v for k, v in sem1_scores.items() if SUBJECTS[k]['counts_gpa'] and v >= 0}
                        new_diem_tb = round(np.mean(list(scores_for_avg.values())), 2) if scores_for_avg else 0.0
                        new_xep_loai = calculate_grade(new_diem_tb)
                        
                        update_query = f"""UPDATE grades SET 
                            {', '.join([f'{k} = ?' for k in SEMESTER_1_SUBJECTS])},
                            diem_tb = ?, xep_loai = ?, updated_at = ?
                            WHERE id = ?"""
                        
                        values = [float(sem1_scores[k]) for k in SEMESTER_1_SUBJECTS]
                        values.extend([new_diem_tb, new_xep_loai, datetime.now(), sem1_id])
                        c.execute(update_query, values)
                    
                    # Cập nhật HK2 nếu có
                    if not sem2_data.empty:
                        sem2_id = sem2_data.iloc[0]['id']
                        scores_for_avg = {k: v for k, v in sem2_scores.items() if SUBJECTS[k]['counts_gpa'] and v >= 0}
                        new_diem_tb = round(np.mean(list(scores_for_avg.values())), 2) if scores_for_avg else 0.0
                        new_xep_loai = calculate_grade(new_diem_tb)
                        
                        update_query = f"""UPDATE grades SET 
                            {', '.join([f'{k} = ?' for k in SEMESTER_2_SUBJECTS])},
                            diem_tb = ?, xep_loai = ?, updated_at = ?
                            WHERE id = ?"""
                        
                        values = [float(sem2_scores[k]) for k in SEMESTER_2_SUBJECTS]
                        values.extend([new_diem_tb, new_xep_loai, datetime.now(), sem2_id])
                        c.execute(update_query, values)
                    
                    conn.commit()
                    st.success("Đã cập nhật điểm thành công!")
                    st.rerun()
        else:
            st.warning("Không tìm thấy sinh viên phù hợp.")

    if show_delete:
        st.divider()
        st.subheader("Xóa điểm sinh viên")
        delete_options = {
            row['id']: f"{row['mssv']} - {row['student_name']} - HK{int(row['semester'])} - ĐTB {row['diem_tb']:.2f}"
            for _, row in df.iterrows()
        }
        delete_mode = st.radio("Chế độ xóa", ["Xóa 1", "Xóa nhiều"], horizontal=True)
        
        if delete_mode == "Xóa 1":
            del_id = st.selectbox("Chọn bản ghi", delete_options.keys(), format_func=lambda x: delete_options[x])
            if st.checkbox("Xác nhận xóa"):
                if st.button("Xóa", type="primary"):
                    delete_grade(conn, del_id)
                    st.success("Đã xóa bản ghi!")
                    st.rerun()
        else:
            del_ids = st.multiselect("Chọn các bản ghi", delete_options.keys(), format_func=lambda x: delete_options[x])
            if del_ids and st.checkbox("Xác nhận xóa tất cả"):
                if st.button("Xóa tất cả", type="primary"):
                    delete_grades_batch(conn, del_ids)
                    st.success(f"Đã xóa {len(del_ids)} bản ghi!")
                    st.rerun()


