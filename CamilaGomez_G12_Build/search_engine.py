import time
balance_data = {
    "Camila": {
        "focus_score": 55,
        "stress_level": "moderate",
        "weekly_logs": [
            {"day": "Monday", "focus": 60},
            {"day": "Tuesday", "focus": 50},
            {"day": "Wednesday", "focus": 65}
        ]
    },
    "Student2": {
        "focus_score": 75,
        "stress_level": "low",
        "weekly_logs": [
            {"day": "Monday", "focus": 70},
            {"day": "Tuesday", "focus": 80},
            {"day": "Wednesday", "focus": 75}
        ]
    }
}


def search_balance(data, query):
    query = query.lower()
    results = {}

    for student, information in data.items():
        if query in student.lower():
            results[student] = information

    return results