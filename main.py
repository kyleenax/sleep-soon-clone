
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Welcome route (first page where user can start the process)
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route to enter sleep hours
@app.route('/sleep')
def sleep():
    return render_template('sleep.html')

# Route to handle sleep hours submission and move to task entry
@app.route('/tasks', methods=['POST'])
def tasks():
    sleep_hours = request.form.get('sleep')

    # Validate sleep hours (must be a non-negative number)
    if sleep_hours.isdigit() and int(sleep_hours) >= 0:
        session['sleep_hours'] = int(sleep_hours)  # Store sleep hours in session
        return render_template('tasks.html')  # Render the task entry page
    else:
        return "Please enter a valid sleep duration.", 400

# Route to generate the schedule after task entry
@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    try:
        # Retrieve task inputs from the form
        task1_name = request.form['task1']
        task1_duration = int(request.form['task1_duration'])
        task2_name = request.form['task2']
        task2_duration = int(request.form['task2_duration'])
        task3_name = request.form['task3']
        task3_duration = int(request.form['task3_duration'])

        # Get sleep hours from session
        sleep_hours = session.get('sleep_hours')

        # Validate task durations (must be positive numbers)
        if task1_duration < 0 or task2_duration < 0 or task3_duration < 0:
            return "Durations must be positive.", 400

        # Ensure the total time doesn't exceed 24 hours
        total_time = task1_duration + task2_duration + task3_duration + sleep_hours
        if total_time > 24:
            return "The total duration of tasks and sleep cannot exceed 24 hours.", 400

        # Generate the schedule and render it on the HTML page
        schedule = [
            {"name": "Sleep", "start": "00:00", "end": f"{sleep_hours:02}:00", "duration": sleep_hours},
            {"name": task1_name, "start": f"{sleep_hours:02}:00", "end": f"{sleep_hours + task1_duration:02}:00", "duration": task1_duration},
            {"name": task2_name, "start": f"{sleep_hours + task1_duration:02}:00", "end": f"{sleep_hours + task1_duration + task2_duration:02}:00", "duration": task2_duration},
            {"name": task3_name, "start": f"{sleep_hours + task1_duration + task2_duration:02}:00", "end": f"{sleep_hours + task1_duration + task2_duration + task3_duration:02}:00", "duration": task3_duration},
        ]

        return render_template('schedule.html', schedule=schedule)
    except ValueError:
        return "Invalid input. Please enter valid task durations.", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

