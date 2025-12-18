# app.py

import streamlit as st
from config.styles import PREMIUM_SIDEBAR
from database.connection import init_db
from pages.login import login_page
from pages.teacher_dashboard import teacher_dashboard
from pages.student_dashboard import student_dashboard

def main():
    st.set_page_config(
        page_title="Quản lý điểm sinh viên", 
        page_icon="📚", 
        layout="wide"
    )
    
    # Apply styles
    st.markdown(PREMIUM_SIDEBAR, unsafe_allow_html=True)
    
    # Initialize database
    conn = init_db()
    
    # Session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Routing
    if not st.session_state['logged_in']:
        login_page(conn)
    else:
        if st.session_state['role'] == 'teacher':
            teacher_dashboard(conn)
        else:
            student_dashboard(conn)

if __name__ == "__main__":
    main()
