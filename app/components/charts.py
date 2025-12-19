# components/charts.py

import streamlit as st
import plotly.express as px
import pandas as pd
from config.settings import SUBJECTS

def show_dashboard(df):
    st.title("Dashboard Tổng quan")
    
    if df.empty:
        st.warning("Chưa có dữ liệu.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tổng sinh viên", df['mssv'].nunique())
    with col2:
        st.metric("Điểm TB", f"{df['diem_tb'].mean():.2f}")
    with col3:
        st.metric("Cao nhất", f"{df['diem_tb'].max():.2f}")
    with col4:
        st.metric("Thấp nhất", f"{df['diem_tb'].min():.2f}")
    
    st.subheader("Thống kê theo học kỳ")
    col1, col2 = st.columns(2)
    with col1:
        sem1_count = len(df[df['semester'] == 1])
        st.metric("Học kỳ 1", f"{sem1_count} bản ghi")
    with col2:
        sem2_count = len(df[df['semester'] == 2])
        st.metric("Học kỳ 2", f"{sem2_count} bản ghi")
    
    st.subheader("Thống kê theo xếp loại")
    xep_loai_counts = df['xep_loai'].fillna('Chưa xếp loại').value_counts()
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(values=xep_loai_counts.values, names=xep_loai_counts.index, 
                    title='Phân bố xếp loại')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(x=xep_loai_counts.index, y=xep_loai_counts.values,
                    title='Số lượng theo xếp loại', labels={'x': 'Xếp loại', 'y': 'Số lượng'})
        st.plotly_chart(fig, use_container_width=True)

def show_charts(df):
    st.title("Biểu đồ phân tích điểm sinh viên")

    if df.empty:
        st.warning("Chưa có dữ liệu để phân tích.")
        return

    # 1️ Điểm trung bình theo lớp (Bar Chart)
    st.subheader("Điểm trung bình theo lớp")
    class_avg = df.groupby('class_name')['diem_tb'].mean().reset_index()
    fig1 = px.bar(
        class_avg, x='class_name', y='diem_tb',
        title='Điểm TB trung bình theo lớp',
        color='diem_tb', text='diem_tb',
        labels={'class_name':'Lớp', 'diem_tb':'Điểm TB'}
    )
    fig1.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

    # 2️ Phân bố xếp loại (Pie Chart)
    st.subheader("Tỷ lệ xếp loại sinh viên")
    fig2 = px.pie(
        df, names='xep_loai', title='Tỷ lệ xếp loại học lực', hole=0.3
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3 Điểm trung bình các môn học (Line Chart)
    st.subheader("Điểm trung bình các môn học")
    subject_avg = []
    for key, info in SUBJECTS.items():
        if info['counts_gpa'] and key in df.columns:
            avg = pd.to_numeric(df[key], errors='coerce').mean()
            if pd.notna(avg):
                subject_avg.append({'Môn': info['name'], 'Điểm TB': float(avg)})

    if subject_avg:
        subject_df = pd.DataFrame(subject_avg)
        fig3 = px.line(
            subject_df, x='Môn', y='Điểm TB', markers=True,
            title='Điểm TB trung bình các môn học',
            text='Điểm TB'
        )
        st.plotly_chart(fig3, use_container_width=True)

    # 4️ Điểm TB theo học kỳ (Bar Chart)
    st.subheader("Điểm trung bình theo học kỳ")
    semester_avg = df.groupby('semester')['diem_tb'].mean().reset_index()
    semester_avg['Học kỳ'] = semester_avg['semester'].map({1: 'Học kỳ 1', 2: 'Học kỳ 2'})
    fig4 = px.bar(
        semester_avg, x='Học kỳ', y='diem_tb', color='diem_tb',
        title='Điểm TB trung bình theo học kỳ', text='diem_tb',
        labels={'diem_tb':'Điểm TB'}
    )
    fig4.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)

    # 5️ Phân bố điểm TB (Histogram)
    st.subheader("Phân bố điểm trung bình")
    fig5 = px.histogram(
        df, x='diem_tb', nbins=20, title='Phân bố điểm TB',
        labels={'diem_tb':'Điểm TB'}, color_discrete_sequence=['#0abde3']
    )
    st.plotly_chart(fig5, use_container_width=True)
