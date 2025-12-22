# utils/calculations.py

import numpy as np
import pandas as pd
from config.settings import SUBJECTS

def calculate_grade(score):
    try:
        s = float(score)
    except Exception:
        s = 0.0
    if s >= 9.0: return 'Xuất sắc'
    elif s >= 8.0: return 'Giỏi'
    elif s >= 7.0: return 'Khá'
    elif s >= 5.5: return 'Trung bình'
    elif s >= 4.0: return 'Yếu'
    else: return 'Kém'

def calculate_average(row):
    scores = []
    for key, info in SUBJECTS.items():
        if info['counts_gpa']:
            val = row.get(key)
            try:
                num = float(val) if pd.notna(val) else np.nan
            except Exception:
                num = np.nan
            if pd.notna(num) and num >= 0:
                scores.append(num)
    return round(float(np.mean(scores)), 2) if scores else 0.0

def get_ranking_by_semester(df, semester=None):
    """Xếp hạng sinh viên theo điểm GPA"""
    if df.empty:
        return pd.DataFrame()
    
    if semester == 'all' or semester is None:
        grouped = df.groupby('mssv')
        combined_rows = []
        for mssv, group in grouped:
            semesters = group['semester'].unique().tolist()
            if len(semesters) == 2 and 1 in semesters and 2 in semesters:
                sem1_row = group[group['semester'] == 1].iloc[0]
                sem2_row = group[group['semester'] == 2].iloc[0]
                diem_tb_1 = float(sem1_row['diem_tb']) if pd.notna(sem1_row['diem_tb']) else 0
                diem_tb_2 = float(sem2_row['diem_tb']) if pd.notna(sem2_row['diem_tb']) else 0
                diem_tb_combined = round((diem_tb_1 + diem_tb_2) / 2, 2)
                combined_rows.append({
                    'mssv': mssv,
                    'student_name': sem1_row['student_name'],
                    'class_name': sem1_row['class_name'],
                    'semester': 'Cả 2 kỳ',
                    'diem_tb': diem_tb_combined,
                    'xep_loai': calculate_grade(diem_tb_combined),
                    'diem_tb_hk1': diem_tb_1,
                    'diem_tb_hk2': diem_tb_2
                })
        if not combined_rows:
            return pd.DataFrame()
        result_df = pd.DataFrame(combined_rows)
        result_df = result_df.sort_values('diem_tb', ascending=False).reset_index(drop=True)
        result_df['xep_hang'] = range(1, len(result_df) + 1)
        return result_df
    else:
        semester_df = df[df['semester'] == semester].copy()
        if semester_df.empty:
            return pd.DataFrame()
        semester_df = semester_df.sort_values('diem_tb', ascending=False).reset_index(drop=True)
        semester_df['xep_hang'] = range(1, len(semester_df) + 1)
        return semester_df

