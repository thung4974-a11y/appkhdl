# database/clean.py

import pandas as pd
import numpy as np
from config.settings import SUBJECTS, ACADEMIC_YEAR
from database.grades import load_grades
from utils.calculations import calculate_average, calculate_grade

def normalize_score(value):
    """Chuyển điểm về float hợp lệ [0,10], điểm ngoài miền hoặc lỗi sẽ thành None."""
    try:
        value = float(value)
        if 0 <= value <= 10:
            return round(value, 2)
    except:
        pass
    return None

def clean_data(conn):
    df = load_grades(conn)
    c = conn.cursor()

    original_count = len(df)
    if original_count == 0:
        return 0, 0, 0

    # Chuẩn hóa điểm tất cả các môn
    invalid_scores_count = 0
    for key in SUBJECTS.keys():
        if key in df.columns:
            df[key] = pd.to_numeric(df[key], errors='coerce')
            mask_invalid = (~df[key].between(0, 10)) | (df[key].isna() & df[key].notnull())
            invalid_scores_count += int(mask_invalid.sum())
            df.loc[mask_invalid, key] = np.nan

    # Xóa bản ghi trùng MSSV + học kỳ + năm học
    df_clean = df.drop_duplicates(subset=['mssv', 'semester', 'academic_year'], keep='first')
    removed_duplicates = original_count - len(df_clean)

    # Xóa bản ghi MSSV có nhiều tên khác nhau (giữ bản ghi đầu tiên)
    before = len(df_clean)
    df_clean = df_clean.sort_values(['mssv', 'student_name']).groupby('mssv', as_index=False).first()
    removed_name_conflict = before - len(df_clean)

    # Ghi lại vào DB
    try:
        c.execute("DELETE FROM grades")
        for _, row in df_clean.iterrows():
            diem_tb = calculate_average(row)
            xep_loai = calculate_grade(diem_tb)

            def safe_val(k):
                v = row.get(k)
                return float(v) if pd.notna(v) else None

            params = (
                row.get('mssv', ''), row.get('student_name', ''), row.get('class_name', None),
                int(row.get('semester', 1)) if pd.notna(row.get('semester', 1)) else 1,
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

    total_affected = removed_duplicates + removed_name_conflict + invalid_scores_count
    return removed_duplicates, invalid_scores_count, total_affected
