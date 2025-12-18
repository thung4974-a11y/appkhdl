# database/grades.py

import pandas as pd
import numpy as np
from config.settings import SUBJECTS

def load_grades(conn):
    try:
        df = pd.read_sql_query("SELECT * FROM grades", conn)
        for key in SUBJECTS.keys():
            if key in df.columns:
                df[key] = pd.to_numeric(df[key], errors='coerce')
        if 'diem_tb' in df.columns:
            df['diem_tb'] = pd.to_numeric(df['diem_tb'], errors='coerce').fillna(0.0)
        return df
    except Exception:
        cols = ['id','mssv','student_name','class_name','semester'] + list(SUBJECTS.keys()) + ['diem_tb','xep_loai','academic_year','updated_at']
        return pd.DataFrame(columns=cols)

def save_grade(conn, data):
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO grades (mssv, student_name, class_name, semester, 
                     triet, giai_tich_1, giai_tich_2, tieng_an_do_1, tieng_an_do_2,
                     gdtc, thvp, tvth, phap_luat, logic,
                     diem_tb, xep_loai, academic_year)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)

def delete_grade(conn, grade_id):
    c = conn.cursor()
    c.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
    conn.commit()

def delete_grades_batch(conn, grade_ids):
    c = conn.cursor()
    for grade_id in grade_ids:
        c.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
    conn.commit()
