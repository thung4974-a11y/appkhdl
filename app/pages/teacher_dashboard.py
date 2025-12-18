# pages/teacher_dashboard.py

import streamlit as st
from database.grades import load_grades
from components.charts import show_dashboard, show_charts
from components.tables import manage_grades_new, show_ranking
from components.forms import add_grade_form, import_data, export_data, clean_data_page, manage_users

def teacher_dashboard(connconn, df):
    st.sidebar.title(f"{st.session_state.get('fullname','')}")
    st.sidebar.write("Vai trò: **Giáo viên**")
    
    if st.sidebar.button("Đăng xuất", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    menu = st.sidebar.radio("Menu", [
        "Dashboard",
        "Quản lý điểm",
        "Xếp hạng theo GPA",
        "Thêm điểm",
        "Import dữ liệu",
        "Export dữ liệu",
        "Làm sạch dữ liệu",
        "Quản lý tài khoản",
        "Biểu đồ phân tích"
    ])
    
    df = load_grades(conn)
    
    if menu == "Dashboard":
        show_dashboard(df)
    elif menu == "Quản lý điểm":
        manage_grades_new(conn, df)
    elif menu == "Xếp hạng theo GPA":
        show_ranking(df)
    elif menu == "Thêm điểm":
        add_grade_form(conn)
    elif menu == "Import dữ liệu":
        import_data(conn)
    elif menu == "Export dữ liệu":
        export_data(df)
    elif menu == "Làm sạch dữ liệu":
        clean_data_page(conn, df)
    elif menu == "Quản lý tài khoản":
        manage_users(conn)
    elif menu == "Biểu đồ phân tích":
        show_charts(df)

