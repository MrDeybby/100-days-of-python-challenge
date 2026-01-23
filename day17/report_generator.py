import csv


def read_file(path: str):
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        return [line for line in reader]


def average(*arg):
    return sum(arg) / len(arg)


def make_report(input: str, output: str):
    file = read_file(input)
    with open(output, "w", newline="") as f:
        output_file = csv.writer(f)

        output_file.writerow(
            ["Name", "Math", "Science", "English", "History", "Average", "Status"]
        )

        for student in file:
            math_score = int(student["Math"])
            science_score = int(student["Science"])
            english_score = int(student["English"])
            history_score = int(student["History"])
            student_average = average(
                math_score, science_score, english_score, history_score
            )
            status = "Pass" if student_average >= 70 else "Fail"

            output_file.writerow(
                [
                    student["Name"],
                    math_score,
                    science_score,
                    english_score,
                    history_score,
                    student_average,
                    status,
                ]
            )
    print(f"Report generated and saved to '{output}'")


if __name__ == "__main__":
    make_report("students_scores.csv", "students_report.csv")
