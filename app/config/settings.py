# config/settings.py

SUBJECTS = {
    'triet': {'name': 'Triết', 'counts_gpa': True, 'semester': 1},
    'giai_tich_1': {'name': 'Giải tích 1', 'counts_gpa': True, 'semester': 1, 'mandatory': True},
    'giai_tich_2': {'name': 'Giải tích 2', 'counts_gpa': True, 'semester': 2, 'prerequisite': 'giai_tich_1'},
    'tieng_an_do_1': {'name': 'Tiếng Ấn Độ 1', 'counts_gpa': True, 'semester': 1, 'mandatory': True},
    'tieng_an_do_2': {'name': 'Tiếng Ấn Độ 2', 'counts_gpa': True, 'semester': 2, 'prerequisite': 'tieng_an_do_1'},
    'gdtc': {'name': 'GDTC', 'counts_gpa': False, 'semester': 1},
    'thvp': {'name': 'THVP', 'counts_gpa': True, 'semester': 1},
    'tvth': {'name': 'TVTH', 'counts_gpa': True, 'semester': 2},
    'phap_luat': {'name': 'Pháp luật', 'counts_gpa': True, 'semester': 2},
    'logic': {'name': 'Logic và suy luận toán học', 'counts_gpa': True, 'semester': 2},
}

NEXT_SUBJECTS = {
    'triet': 'phap_luat',
    'giai_tich_1': 'giai_tich_2',
    'tieng_an_do_1': 'tieng_an_do_2',
    'phap_luat': 'tu_tuong',
    'giai_tich_2': 'giai_tich_3',
    'tieng_an_do_2': 'tieng_an_do_3',
}

SEMESTER_1_SUBJECTS = ['triet', 'giai_tich_1', 'tieng_an_do_1', 'gdtc', 'thvp']
SEMESTER_2_SUBJECTS = ['giai_tich_2', 'tieng_an_do_2', 'tvth', 'phap_luat', 'logic']
ACADEMIC_YEAR = 1
DB_PATH = 'student_grades.db'
