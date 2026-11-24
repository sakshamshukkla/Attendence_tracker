# Attendance Tracker and Shortage Predictor (simple version)
# Data is saved in attendance.csv  ->  subject, attended, total

import csv

FILE_NAME = "attendance.csv"
REQUIRED = 75     # required attendance percentage


def load_data():
    """Read the file and return a dictionary like {"Maths": [8, 10]}"""
    data = {}
    try:
        file = open(FILE_NAME, "r")
        reader = csv.reader(file)
        next(reader)                      # skip the heading row
        for row in reader:
            data[row[0]] = [int(row[1]), int(row[2])]
        file.close()
    except FileNotFoundError:
        pass                              # first run, no file yet
    return data


def save_data(data):
    """Write the dictionary into the file."""
    file = open(FILE_NAME, "w", newline="")
    writer = csv.writer(file)
    writer.writerow(["subject", "attended", "total"])
    for subject in data:
        writer.writerow([subject, data[subject][0], data[subject][1]])
    file.close()


def get_number(message, low, high):
    """Keep asking until the user types a valid number."""
    while True:
        try:
            number = int(input(message))
            if number >= low and number <= high:
                return number
            print("Number must be between", low, "and", high)
        except ValueError:
            print("Please enter a number only.")


def choose_subject(data):
    """Show the subjects and return the one the user picks."""
    if len(data) == 0:
        print("No subjects added yet.")
        return None
    names = list(data.keys())
    for i in range(len(names)):
        print(i + 1, ".", names[i])
    choice = get_number("Choose subject number: ", 1, len(names))
    return names[choice - 1]


def add_subject(data):
    name = input("Enter subject name: ").strip().title()
    if name == "":
        print("Name cannot be empty.")
    elif name in data:
        print("Subject already exists.")
    else:
        data[name] = [0, 0]               # [attended, total]
        save_data(data)
        print("Subject added.")


def mark_attendance(data):
    subject = choose_subject(data)
    if subject is None:
        return
    status = get_number("Enter 1 for Present, 2 for Absent: ", 1, 2)
    data[subject][1] = data[subject][1] + 1        # total always increases
    if status == 1:
        data[subject][0] = data[subject][0] + 1    # attended only if present
    save_data(data)
    print("Attendance saved.")


def calculate_percentage(attended, total):
    if total == 0:
        return 0
    return attended * 100 / total


def view_attendance(data):
    if len(data) == 0:
        print("No subjects added yet.")
        return
    for subject in data:
        attended = data[subject][0]
        total = data[subject][1]
        percent = calculate_percentage(attended, total)
        print(subject, "-", attended, "/", total, "=", round(percent, 1), "%")


def shortage_predictor(data):
    subject = choose_subject(data)
    if subject is None:
        return
    attended = data[subject][0]
    total = data[subject][1]

    if total == 0:
        print("No classes recorded yet.")
        return

    percent = calculate_percentage(attended, total)
    print(subject, "attendance is", round(percent, 1), "%")

    if percent < REQUIRED:
        # count how many classes must be attended in a row
        count = 0
        while calculate_percentage(attended, total) < REQUIRED:
            attended = attended + 1
            total = total + 1
            count = count + 1
        print("Shortage! Attend the next", count, "classes to reach", REQUIRED, "%")
    else:
        # count how many classes can be missed
        count = 0
        while calculate_percentage(attended, total + 1) >= REQUIRED:
            total = total + 1
            count = count + 1
        print("Safe! You can miss", count, "more classes.")


def main():
    data = load_data()
    while True:
        print("\n--- Attendance Tracker ---")
        print("1. Add subject")
        print("2. Mark attendance")
        print("3. View attendance")
        print("4. Shortage predictor")
        print("5. Exit")
        choice = get_number("Enter your choice: ", 1, 5)

        if choice == 1:
            add_subject(data)
        elif choice == 2:
            mark_attendance(data)
        elif choice == 3:
            view_attendance(data)
        elif choice == 4:
            shortage_predictor(data)
        else:
            print("Goodbye!")
            break


main()
