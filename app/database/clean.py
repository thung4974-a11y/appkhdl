# database/clean.py

import pandas as pd
import numpy as np
from config.settings import SUBJECTS, ACADEMIC_YEAR
from database.grades import load_grades
from utils.calculations import calculate_average, calculate_grade


def normalize_score(value):
     try:
        score = float(value)
        if 0 <= score <= 10:
            return round(score, 2)
        return None
    except (ValueError, TypeError):
        return None


def normalize_text(text):
    if text is None:
        return None
    return str(text).strip()


def clean_data(conn):
    df = load_grades(conn)
    c = conn.cursor()

    original_count = len(df)
    if original_count == 0:
        return 0, 0, 0

    # 1️⃣ Chuẩn hoá kiểu dữ liệu điểm
    for key in SUBJECTS.keys():
        if key in df.columns:
            df[key] = df[key].apply(normalize_score)

    # 2️⃣ Đếm số điểm bị loại (ngoài [0,10])
    invalid_score_count = int(df[SUBJECTS.keys()].isna().sum().sum())

    # 3️⃣ Chuẩn hoá text
    for col in ["mssv", "student_name", "class_name"]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)

    # 4️⃣ Xoá trùng đúng NGHIỆP VỤ (mssv + semester + year)
    df_clean = df.drop_duplicates(
        subset=["mssv", "semester", "academic_year"],
        keep="first"
    )
    removed_duplicates = original_count - len(df_clean)

    try:
        # 5️⃣ Chỉ xoá dữ liệu NĂM HỌC HIỆN TẠI
        c.execute(
            "DELETE FROM grades WHERE academic_year = ?",
            (ACADEMIC_YEAR,)
        )

        # 6️⃣ Ghi lại dữ liệu đã làm sạch
        for _, row in df_clean.iterrows():
            diem_tb = calculate_average(row)
            xep_loai = calculate_grade(diem_tb)

            params = (
                row.get("mssv"),
                row.get("student_name"),
                row.get("class_name"),
                int(row.get("semester", 1)),
                *(row.get(k) for k in SUBJECTS.keys()),
                float(diem_tb),
                xep_loai,
                int(ACADEMIC_YEAR)
            )

            placeholders = ",".join(["?"] * len(params))

            c.execute(
                f"""
                INSERT INTO grades (
                    mssv, student_name, class_name, semester,
                    {",".join(SUBJECTS.keys())},
                    diem_tb, xep_loai, academic_year
                )
                VALUES ({placeholders})
                """,
                params
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    return removed_duplicates, invalid_score_count, original_count - len(df_clean)

