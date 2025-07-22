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
                "name": "GAA-1",
                "max": 100
            },
            {
                "id": 2,
                "name": "GAA-2",
                "max": 100
            },
            {
                "id": 3,
                "name": "Quiz-1",
                "max": 100
            },
            {
                "id": 4,
                "name": "OPPE-1",
                "max": 100
            },
            {
                "id": 5,
                "name": "OPPE-2",
                "max": 100
            },
            {
                "id": 6,
                "name": "Bonus",
                "max": 2
            }
        ]
    return data

def calc_score(code, marks_list):

    if code == "CS1002":
        GAA1 = marks_list["1"]
        GAA2 = marks_list["2"]
        Q = marks_list["3"]
        OP1 = marks_list["4"]
        OP2 = marks_list["5"]
        Bonus = marks_list["6"]

        F = 0

        score = 0.1*GAA1 + 0.1*GAA2 + 0.2*Q + 0.4*F + 0.25*max(OP1, OP2) + 0.15*min(OP1, OP2) + Bonus
    else:
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
    grade_verdict = {}
    for next_marks, next_grade in zip(range(40, 100, 10), grades):
        if score < next_marks:
            if next_marks - score <= 100:
                marks_coordinates[next_grade] = round(next_marks - score, 2)
            else:
                grade_verdict[next_grade] = False
        else:
            if grade != next_grade:
                grade_verdict[next_grade] = True

    grade_verdict = sorted(list( grade_verdict.items()))

    print(marks_coordinates)

    current_status = {
        "score": score, 
        "grade": grade, 
        "verdict": pass_or_not,
        "grade_verdict": grade_verdict
    }

    print(current_status)

    resources = {}

    return current_status, marks_coordinates, resources
