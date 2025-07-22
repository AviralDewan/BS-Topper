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
                "name": "GAA - Objective",
                "max": 100
            },
            {
                "id": 2,
                "name": "GAA - Programming",
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

''' 
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
'''

def calc_score(code, marks_list):
    grade_thresholds = [("S", 90), ("A", 80), ("B", 70), ("C", 60), ("D", 50), ("E", 40)]
    
    def get_grade(score):
        if score >= 90: return 'S'
        elif score >= 80: return 'A'
        elif score >= 70: return 'B'
        elif score >= 60: return 'C'
        elif score >= 50: return 'D'
        elif score >= 40: return 'E'
        else: return 'U'

    def calculate_needed_final_CS1002(GAA1, GAA2, Q, OP1, OP2, Bonus, target_score):
        fixed_score = (
            0.1 * GAA1 + 0.1 * GAA2 + 0.2 * Q +
            0.25 * max(OP1, OP2) + 0.15 * min(OP1, OP2) + Bonus
        )
        required_F = (target_score - fixed_score) / 0.4
        return round(required_F, 2) if 0 <= required_F <= 100 else False

    def calculate_needed_final_other(GAA, Q1, Q2, Bonus, target_score):
        needed_scores = []

        # Option 1: 0.1*GAA + 0.6*F + 0.2*max(Q1, Q2) + Bonus
        fixed1 = 0.1 * GAA + 0.2 * max(Q1, Q2) + Bonus
        required_F1 = (target_score - fixed1) / 0.6
        if 0 <= required_F1 <= 100:
            needed_scores.append(round(required_F1, 2))

        # Option 2: 0.1*GAA + 0.4*F + 0.2*Q1 + 0.3*Q2 + Bonus
        fixed2 = 0.1 * GAA + 0.2 * Q1 + 0.3 * Q2 + Bonus
        required_F2 = (target_score - fixed2) / 0.4
        if 0 <= required_F2 <= 100:
            needed_scores.append(round(required_F2, 2))

        return min(needed_scores) if needed_scores else False

    marks_coordinates = {}
    grade_verdict = []

    if code == "CS1002":
        GAA1 = marks_list["1"]
        GAA2 = marks_list["2"]
        Q = marks_list["3"]
        OP1 = marks_list["4"]
        OP2 = marks_list["5"]
        Bonus = marks_list["6"]
        F = 0  # Assume not attempted yet

        # Current score
        score = (
            0.1 * GAA1 + 0.1 * GAA2 + 0.2 * Q +
            0.4 * F + 0.25 * max(OP1, OP2) + 0.15 * min(OP1, OP2) + Bonus
        )

        for grade, threshold in grade_thresholds:
            needed = calculate_needed_final_CS1002(GAA1, GAA2, Q, OP1, OP2, Bonus, threshold)
            marks_coordinates[grade] = needed
            if needed is not False:
                grade_verdict.append((grade, True))
            else:
                grade_verdict.append((grade, False))

    else:
        GAA = marks_list["1"]
        Q1 = marks_list["2"]
        Q2 = marks_list["3"]
        Bonus = marks_list["4"]
        F = 0

        score1 = 0.1 * GAA + 0.6 * F + 0.2 * max(Q1, Q2) + Bonus
        score2 = 0.1 * GAA + 0.4 * F + 0.2 * Q1 + 0.3 * Q2 + Bonus
        score = max(score1, score2)

        for grade, threshold in grade_thresholds:
            needed = (
                calculate_needed_final_CS1002(GAA1, GAA2, Q, OP1, OP2, Bonus, threshold) 
                if code == "CS1002" 
                else calculate_needed_final_other(GAA, Q1, Q2, Bonus, threshold)
            )
            marks_coordinates[grade] = needed
            if score >= threshold:
                grade_verdict.append((grade, True))  
            elif needed is False:
                grade_verdict.append((grade, False)) 

    score = round(score, 2)
    grade = get_grade(score)
    pass_or_not = grade != 'U'

    current_status = {
        "score": score,
        "grade": grade,
        "verdict": pass_or_not,
        "grade_verdict": sorted(grade_verdict) 
    }

    print(current_status, marks_coordinates)

    resources = {}

    return current_status, marks_coordinates, resources

