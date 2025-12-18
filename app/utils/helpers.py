# utils/helpers.py

import pandas as pd
from config.settings import SUBJECTS, SEMESTER_1_SUBJECTS, SEMESTER_2_SUBJECTS, NEXT_SUBJECTS
from database.grades import load_grades

def can_take_semester_2(conn, mssv):
    df = load_grades(conn)
    student_sem1 = df[(df['mssv'] == mssv) & (df['semester'] == 1)]
    
    if student_sem1.empty:
        return False, "Chưa có điểm học kỳ 1"
    
    row = student_sem1.iloc[0]
    try:
        giai_tich_1 = float(row.get('giai_tich_1') or 0)
    except Exception:
        giai_tich_1 = 0
    try:
        tieng_an_do_1 = float(row.get('tieng_an_do_1') or 0)
    except Exception:
        tieng_an_do_1 = 0
    avg = (giai_tich_1 + tieng_an_do_1) / 2.0
    
    if avg >= 4:
        return True, f"Đủ điều kiện (TB: {avg:.2f})"
    else:
        return False, f"Chưa đủ điều kiện (TB: {avg:.2f} < 4)"

def generate_study_suggestions(row, semester):
    """Tạo gợi ý học tập dựa trên điểm số"""
    suggestions = {
        'hoc_lai': [],
        'cai_thien': [],
        'can_hoc': [],
        'hoc_tiep': []
    }
    
    current_subjects = SEMESTER_1_SUBJECTS if semester == 1 else SEMESTER_2_SUBJECTS
    
    for key in current_subjects:
        info = SUBJECTS[key]
        score = row.get(key)
        
        try:
            score_val = float(score) if pd.notna(score) else None
        except:
            score_val = None
        
        if score_val is None:
            suggestions['can_hoc'].append(info['name'])
        elif score_val < 4:
            suggestions['hoc_lai'].append(f"{info['name']} ({score_val:.1f})")
        elif score_val < 6:
            suggestions['cai_thien'].append(f"{info['name']} ({score_val:.1f})")
        
        if score_val is not None and score_val >= 4 and key in NEXT_SUBJECTS:
            next_subject = NEXT_SUBJECTS[key]
            if semester == 1:
                next_name = {
                    'phap_luat': 'Pháp luật',
                    'giai_tich_2': 'Giải tích 2',
                    'tieng_an_do_2': 'Tiếng Ấn Độ 2'
                }.get(next_subject, next_subject)
            else:
                next_name = {
                    'tu_tuong': 'Tư tưởng (Năm 2)',
                    'giai_tich_3': 'Giải tích 3 (Năm 2)',
                    'tieng_an_do_3': 'Tiếng Ấn Độ 3 (Năm 2)'
                }.get(next_subject, next_subject)
            suggestions['hoc_tiep'].append(f"{next_name}")
    
    return suggestions
