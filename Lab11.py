import os
import matplotlib.pyplot as plt


def read_students():
    students = {}
    with open('data/students.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line or ',' not in line:  # Skip empty or invalid lines
                continue
            student_id, student_name = line.split(',', 1)  # Ensure correct unpacking
            students[student_id.strip()] = student_name.strip()
    return students


def read_assignments():
    assignments = {}
    with open('data/assignments.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.count(',') < 2:  # Ensure line has at least 3 parts
                continue
            assignment_name, assignment_id, point_value = line.split(',', 2)
            assignments[assignment_id.strip()] = (assignment_name.strip(), int(point_value.strip()))
    return assignments


def read_submission():
    submissions = {}
    submissions_dir = 'data/submissions'

    if not os.path.exists(submissions_dir):
        print(f"Error: Submissions directory '{submissions_dir}' not found.")
        return submissions

    for file_name in os.listdir(submissions_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(submissions_dir, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.count(',') != 2:
                        # Skip lines that do not have exactly 2 commas (3 values)
                        continue
                    student_id, assignment_id, score = line.split(',')
                    if assignment_id not in submissions:
                        submissions[assignment_id] = []
                    submissions[assignment_id].append((student_id.strip(), float(score.strip())))

    return submissions

def calculate_grade(student_name, students, assignments, submission):
    student_id = next((sid for sid, name in students.items() if name.lower() == student_name.lower()), None)
    if not student_id:
        print("Student not found")
        return

    total_score = sum((score /100)* assignments[assignment_id][1]
                      for assignment_id, submission_list in submission.items()
                      for sid, score in submission_list if sid == student_id)

    grade_percent = round((total_score / 1000)*100)
    print(f"{grade_percent}%")



def assignment_stats(assignment_names, assignments, submission):
    assignment_id = next((aid for aid, (name, _) in assignments.items() if name.lower() == assignment_name.lower()),
                         None)
    if not assignment_id:
        print("Assignment not found")
        return

    scores = [score for _, score in submissions.get(assignment_id, [])]
    if not scores:
        print("No submissions found for this assignment")
        return

    min_score, max_score, avg_score = min(score), max(score), sum(score)/len(score)
    print(f"min:{min_score}%")
    print(f"max:{max_score}%")
    print(f"avg:{round(avg_score)}%")


def assignment_graph(assignment_name, assignments, submission):
    assignmnet_id = next((aid for aid, (name, _) in assignments.items() if name.lower() == assignment_name.lower()), None)
    if not assignment_id:
        print("Assignment not found")
        return


    scores = [score for sid, score in submission.get(assignment_id,[])]
    if not scores:
        print("No submission found for this assignment")
        return

    plt.hist(scores, bins=[0,25,50,75,100])
    plt.title(f"Score Distribution for {assignmnet_name}")
    plt.xlabel("Score Percentage")
    plt.ylabel("Number of Students")
    plt.show()



def main():
    students = read_students()
    assignments = read_assignments()
    submision = read_submission()

    while True:
        print("1. Student grade")
        print("2. Assignment grade")
        print("3. Submission grade")
        choice = (input("Enter your choice: "))


        if choice == "1":
            student_name = input("What is the student's name: ")
            calculate_grade(student_name, students, assignments, submision)
            break

        elif choice == "2":
            assignment_name = input("What is the assignment name: ")
            assignment_stats(assignment_name, assignments, submision)
            break

        elif  choice == "3":
            assignment_name = input("What is the assignment name: ")
            assignment_graph(assignment_name, assignments, submision)
            break



if __name__ == "__main__":
    main()

