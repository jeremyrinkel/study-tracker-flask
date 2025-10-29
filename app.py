# Student Study Tracker
from flask import Flask, request, render_template_string

app = Flask(__name__)

study_log = {}

@app.route('/')
def home():
    return render_template_string('''
        <h1>Study Tracker</h1>
        <form action="/add" method="post">
            Subject: <input name="subject"><br>
            Day: <input name="day"><br>
            Minutes: <input name="minutes"><br>
            <button type="submit">Add Session</button>
        </form>
        <a href="/summary">View Summary</a>
    ''')

@app.route('/add', methods=['POST'])
def add():
    subject = request.form['subject']
    day = request.form['day']
    minutes = int(request.form['minutes'])
    study_log.setdefault(subject, []).append((day, minutes))
    return "Session added! <a href='/'>Back</a>"

@app.route('/summary')
def summary():
    output = "<h2>Weekly Summary</h2>"
    for subject, sessions in study_log.items():
        total = sum(m for d, m in sessions)
        output += f"{subject}: {total} minutes ({len(sessions)} sessions)<br>"
    return output + "<br><a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(debug=True)

def add_study_time(study_log, subject, day, minutes):
    """Add a study session to the tracker."""
    if subject not in study_log:
        study_log[subject] = []
    study_log[subject].append((day, minutes))  # tuple of (day, minutes)


def total_minutes_for_subject(study_log, subject):
    """Return total study time for a specific subject."""
    if subject not in study_log:
        return 0
    return sum(minutes for day, minutes in study_log[subject])


def weekly_summary(study_log):
    """Print total minutes per subject."""
    print("\n--- Weekly Study Summary ---")
    for subject, sessions in study_log.items():
        total = total_minutes_for_subject(study_log, subject)
        print(f"{subject}: {total} minutes ({len(sessions)} sessions)")


def most_studied_subject(study_log):
    """Find and return the subject with the most total minutes."""
    if not study_log:
        return None
    totals = {subject: total_minutes_for_subject(study_log, subject)
              for subject in study_log}
    return max(totals, key=totals.get)


# Main program
def main():
    study_log = {}

    while True:
        print("\n1. Add study session")
        print("2. View weekly summary")
        print("3. See most studied subject")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            subject = input("Enter subject: ").title()
            day = input("Enter day of the week: ").title()
            minutes = int(input("Enter minutes studied: "))
            add_study_time(study_log, subject, day, minutes)
            print(f"Added {minutes} minutes for {subject} on {day}.")

        elif choice == "2":
            weekly_summary(study_log)

        elif choice == "3":
            subject = most_studied_subject(study_log)
            if subject:
                print(f"\nMost studied subject: {subject} "
                      f"({total_minutes_for_subject(study_log, subject)} minutes)")
            else:
                print("No study data yet.")

        elif choice == "4":
            print("Goodbye! Keep studying smart!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()



