course_list = ["MA1001", "MA1002", "CS1001", "HS1001", "MA1003", "MA1004", "CS1002", "HS1002"]

def test_fields(code):
    if code in ["MA1001", "HS1001", "CS1001", "MA1003", "HS1002", "MA1002", "MA1004"]:
        # GAA, Q1, Q2, Bonus
        data = [
            {
                "id": 1,
                "name": "GAA",
                "max": 100
            },
            {
                "id": 2,
                "name": "Quiz-1",
                "max": 100
            },
            {
                "id": 3,
                "name": "Quiz-2",
                "max": 100
            },
            {
                "id": 4,
                "name": "Bonus",
                "max": 2
            }
        ]
    elif code == "CS1002":
        # GAA, Q1, OP1, OP2, Bonus
         data = [ 
            {
                "id": 1,
                "name": "GAA",
                "max": 100
            },
            {
                "id": 2,
                "name": "Quiz-1",
                "max": 100
            },
            {
                "id": 3,
                "name": "OPPE-1",
                "max": 100
            },
            {
                "id": 4,
                "name": "OPPE-2",
                "max": 100
            },
            {
                "id": 5,
                "name": "Bonus",
                "max": 2
            }
        ]
    return data

def calc_score(code, marks_list):

    if code == "CS1002":
        pass

    GAA = marks_list["1"]
    Q1 = marks_list["2"]
    Q2 = marks_list["3"]
    Bonus = marks_list["4"]

    F = 0

    score = 0.1*GAA + max (0.6*F + 0.2*max(Q1, Q2),  0.4*F + 0.2*Q1 + 0.3*Q2) + Bonus
    if score > 100:
        score = 100
    score = round(score, 2)

    grade = 'U'

    if score >= 90:
        grade = 'S'
    elif score >= 80:
        grade = 'A'
    elif score >= 70:
        grade = 'B'
    elif score >= 60:
        grade = 'C'
    elif score >= 50:
        grade = 'D'
    elif score >= 40:
        grade = 'E'
    
    pass_or_not = True
    if grade == 'U':
        pass_or_not = False
    
    marks_coordinates = {}
    grades = ["E", "D", "C", "B", "A", "S"]
    cant_achieve = []
    already_achieved = []
    for next_marks, next_grade in zip(range(40, 100, 10), grades):
        if score < next_marks:
            if next_marks - score <= 100:
                marks_coordinates[next_grade] = round(next_marks - score, 2)
            else:
                cant_achieve.append(next_grade)
        else:
            already_achieve.append(next_grade)

    current_status = {
        "score": score, 
        "grade": grade, 
        "verdict": pass_or_not,
        "cant_achieve": cant_achieve,
        "already_achieve": already_achieve
    }

    resources = {}

    return current_status, marks_coordinates, resources
