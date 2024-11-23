import os
import sys
import matplotlib.pyplot as plt

def read_students():
    students = {}
    with open('data/students.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            student_id = line[:3]
            student_name = line[3:].strip()
            students[student_id] = student_name
    return students

def read_assignments():
    assignments = {}
    with open('data/assignments.txt', 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            assignment_name = lines[i].strip()
            assignment_id = lines[i + 1].strip()
            point_value = lines[i + 2].strip()
            assignments[assignment_id] = (assignment_name, int(point_value))
    return assignments

def read_submissions():
    submissions = {}
    submissions_dir = 'data/submissions'

    for file_name in os.listdir(submissions_dir):
        file_path = os.path.join(submissions_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('|')
                    if len(parts) != 3:
                        continue
                    student_id, assignment_id, score = parts
                    if assignment_id not in submissions:
                        submissions[assignment_id] = []
                    submissions[assignment_id].append((student_id.strip(), float(score.strip())))
    return submissions

def calculate_grade(student_name, students, assignments, submissions):
    student_id = next((sid for sid, name in students.items() if name.lower().strip() == student_name.lower().strip()), None)
    if not student_id:
        print("Student not found")
        return
    total_score = sum(
        (score / 100) * assignments[assignment_id][1]
        for assignment_id, submission_list in submissions.items()
        for sid, score in submission_list if sid.strip() == student_id
    )
    grade_percent = round((total_score / 1000) * 100)
    print(f"{grade_percent}%")

def assignment_stats(assignment_name, assignments, submissions):
    assignment_id = next(
        (aid for aid, (name, _) in assignments.items() if name.lower().strip() == assignment_name.lower().strip()), None)
    if not assignment_id:
        print("Assignment not found")
        return
    scores = [score for _, score in submissions.get(assignment_id, [])]
    if not scores:
        print("No submissions found for this assignment")
        return
    print(f"Min: {min(scores):.0f}%")
    print(f"Max: {max(scores):.0f}%")
    print(f"Avg: {round(sum(scores) / len(scores))}%")

def assignment_graph(assignment_name, assignments, submissions):
    assignment_id = next(
        (aid for aid, (name, _) in assignments.items() if name.lower().strip() == assignment_name.lower().strip()), None)
    if not assignment_id:
        print("Assignment not found")
        return
    scores = [score for _, score in submissions.get(assignment_id, [])]
    if not scores:
        print("No submissions found for this assignment")
        return
    plt.hist(scores, bins=[0, 25, 50, 75, 100], edgecolor='black')
    plt.title(f"Score Distribution for {assignment_name}")
    plt.xlabel("Score Percentage")
    plt.ylabel("Number of Students")
    plt.show()

def main():
    students = read_students()
    assignments = read_assignments()
    submissions = read_submissions()

    if len(sys.argv) <2:
        print("Usage : script.py <choice> [<student_name>|<assigsnment_name>]")
        return



    while True:
        print("\n1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        choice = input("Enter your choice: ")

        if choice == "1" and len(sys.argv) > 2 :
            student_name = sys.argv[2]
            student_name = input("What is the student's name: ")
            calculate_grade(student_name, students, assignments, submissions)
        elif choice == "2" and len(sys.argv) > 2 :
            assignmnet_name = sys.argv[2]
            assignment_name = input("What is the assignment name: ")
            assignment_stats(assignment_name, assignments, submissions)
        elif choice == "3" and len(sys.argv) > 2 :
            assignment_name = sys.argv[2]
            assignment_name = input("What is the assignment name: ")
            assignment_graph(assignment_name, assignments, submissions)
        else:
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()
