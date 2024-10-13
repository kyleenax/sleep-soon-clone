
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
        sleep_hours = session.get('sleep_hours', 0)  # Default to 0 if not set
        tasks = []
        total_duration = sleep_hours

        # Loop through task inputs to collect names and durations
        for i in range(1, 10):  # Assuming a max of 9 tasks
            task_name = request.form.get(f'task{i}')
            task_duration = request.form.get(f'task{i}_duration')

            if task_name and task_duration:
                task_duration = int(task_duration)
                if task_duration < 0:
                    return "Durations must be positive.", 400
                tasks.append((task_name, task_duration))
                total_duration += task_duration

        # Ensure the total time doesn't exceed 24 hours
        if total_duration > 24:
            return "The total duration of tasks and sleep cannot exceed 24 hours.", 400

        # Generate the schedule
        schedule = []
        current_time = 0  # Start from midnight

        schedule.append({"name": "Sleep", "start": f"{current_time:02}:00", "end": f"{sleep_hours:02}:00", "duration": sleep_hours})
        current_time += sleep_hours

        for task_name, task_duration in tasks:
            schedule.append({"name": task_name, "start": f"{current_time:02}:00", "end": f"{current_time + task_duration:02}:00", "duration": task_duration})
            current_time += task_duration

        return render_template('schedule.html', schedule=schedule)

    except ValueError:
        return "Invalid input. Please enter valid task durations.", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

