# pages/login.py

import streamlit as st
from config.styles import LOGIN_PAGE_BG, LOGIN_FORM_CSS
from database.users import verify_user

def login_page(conn):
    st.markdown(LOGIN_PAGE_BG, unsafe_allow_html=True)
    st.markdown(LOGIN_FORM_CSS, unsafe_allow_html=True)
    
    st.title("Hệ thống Quản lý Điểm Sinh viên")
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        
        if st.button("Đăng nhập", use_container_width=True):
            user = verify_user(conn, username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_id'] = user[0]
                st.session_state['fullname'] = user[3]
                st.session_state['role'] = user[4]
                st.session_state['student_id'] = user[5]
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu!")
