# database/clean.py

import pandas as pd
import numpy as np
from config.settings import SUBJECTS, ACADEMIC_YEAR
from database.grades import load_grades
from utils.calculations import calculate_average, calculate_grade

def clean_data(conn):
    df = load_grades(conn)
    c = conn.cursor()
    
    original_count = len(df)
    if original_count == 0:
        return 0, 0, 0
    
    for key in SUBJECTS.keys():
        if key in df.columns:
            df[key] = pd.to_numeric(df[key], errors='coerce')
    
    negative_fixed = 0
    for key in SUBJECTS.keys():
        if key in df.columns:
            count = int((df[key] < 0).sum())
            negative_fixed += count
            df.loc[df[key] < 0, key] = np.nan
    
    df_clean = df.drop_duplicates(subset=['mssv', 'semester'], keep='first')
    removed_semester = original_count - len(df_clean)
    
    before = len(df_clean)
    df_clean = (
        df_clean.sort_values(["mssv", "student_name"])
                .groupby("mssv", as_index=False)
                .first()
    )
    removed_name_conflict = before - len(df_clean)
    
    try:
        c.execute("DELETE FROM grades")
        for _, row in df_clean.iterrows():
            diem_tb = calculate_average(row)
            xep_loai = calculate_grade(diem_tb)
            
            def safe_val(k):
                v = row.get(k)
                if pd.isna(v):
                    return None
                return float(v) if v != '' else None
            
            params = (
                row.get('mssv', ''), row.get('student_name', ''), row.get('class_name', None),
                int(row.get('semester', 1)) if not pd.isna(row.get('semester', 1)) else 1,
                safe_val('triet'), safe_val('giai_tich_1'), safe_val('giai_tich_2'),
                safe_val('tieng_an_do_1'), safe_val('tieng_an_do_2'),
                safe_val('gdtc'), safe_val('thvp'), safe_val('tvth'),
                safe_val('phap_luat'), safe_val('logic'),
                float(diem_tb), xep_loai, int(ACADEMIC_YEAR)
            )
            
            c.execute(
                '''INSERT INTO grades (mssv, student_name, class_name, semester,
                triet, giai_tich_1, giai_tich_2, tieng_an_do_1, tieng_an_do_2,
                gdtc, thvp, tvth, phap_luat, logic,
                diem_tb, xep_loai, academic_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                params
            )
        
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    
    return removed_semester, removed_name_conflict, negative_fixed
