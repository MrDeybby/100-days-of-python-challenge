import os

FILE_PATH = "student_grades.txt"

while True:
    os.system("cls")
    student_scores = input("Enter student scores separed by comma: ").split(",")
    try:
        student_scores = [int(score) for score in student_scores]
    except ValueError:
        print("All scores must be integers.")
        input("Press Enter to try again...")
    else:
        break


student_grades = [
    "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
    for score in student_scores
]

passing_students = [score for score in student_scores if score >= 70]
failling_students = [score for score in student_scores if score < 70]

print("\n=== Student Grades ===")
for i, (score, grade) in enumerate(zip(student_scores, student_grades), start=1):
    print(f"Student {i}: Score: = {score}, Grade = {grade}")

print("\n=== Passing Students ===")
print(", ".join(map(str, passing_students)))

print("\n=== Failling Students ===")
print(", ".join(map(str, failling_students)))

print(f"\nResults saved to '{FILE_PATH}'.")

with open(FILE_PATH, "w") as file:
    file.write("=== Student Grades ===\n")
    for i, (score, grade) in enumerate(zip(student_scores, student_grades), start=1):
        file.write(f"Student {i}: Score: = {score}, Grade = {grade}\n")

    file.write("\n=== Passing Students ===\n")
    file.write(", ".join(map(str, passing_students)) + "\n")

    file.write("\n=== Failling Students ===\n")
    file.write(", ".join(map(str, failling_students)) + "\n")

print("\n=== Summary ===")
print(f"Total Students: {len(student_scores)}")
print(f"Passing Students: {len(passing_students)}")
print(f"Failling Students: {len(failling_students)}")
