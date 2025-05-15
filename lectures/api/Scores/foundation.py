course_list = ["MA1001", "MA1002", "CS1001", "HS1001", "MA1003", "MA1004", "CS1002", "HS1002"]

def test_fields(code):
    if code in ["MA1001", "HS1001", "CS1001", "MA1003", "HS1002", "MA1002", "MA1004"]:
        # GAA, Q1, Q2, ET, Bonus
        data = [
            {
                "id": 1,
                "name": "GAA",
                "marks": 100
            },
            {
                "id": 2,
                "name": "Quiz-1",
                "marks": 100
            },
            {
                "id": 3,
                "name": "Quiz-2",
                "marks": 100
            },
            {
                "id": 4,
                "name": "End-Term",
                "marks": 100
            },
            {
                "id": 5,
                "name": "Bonus",
                "marks": 100
            }
        ]
    elif code == "CS1002":
        # GAA, Q1, OP1, OP2, ET, Bonus
         data = [ 
            {
                "id": 1,
                "name": "GAA",
                "marks": 100
            },
            {
                "id": 2,
                "name": "Quiz-1",
                "marks": 100
            },
            {
                "id": 3,
                "name": "OPPE-1",
                "marks": 100
            },
            {
                "id": 4,
                "name": "OPPE-2",
                "marks": 100
            },
            {
                "id": 5,
                "name": "End-Term",
                "marks": 100
            },
            {
                "id": 6,
                "name": "Bonus",
                "marks": 100
            }
        ]
    return data
