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
    start_time = request.form.get('start_time')

    # Validate sleep hours (must be a non-negative number)
    if sleep_hours and sleep_hours.isdigit() and int(sleep_hours) >= 0:
        session['sleep_hours'] = int(sleep_hours)  # Store sleep hours in session

        # Validate start time format (should be a valid time in HH:MM format)
        if start_time:
            try:
                hours, minutes = map(int, start_time.split(':'))
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    session['start_time'] = start_time  # Store start time in session
                    return render_template('tasks.html')  # Render the task entry page
                else:
                    return "Invalid start time. Please enter a valid time in HH:MM format.", 400
            except ValueError:
                return "Invalid start time. Please enter a valid time in HH:MM format.", 400
        else:
            return "Start time is required.", 400
    else:
        return "Please enter a valid sleep duration.", 400

# Route to generate the schedule after task entry
@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    try:
<<<<<<< Updated upstream
        sleep_hours = session.get('sleep_hours', 0)  # Default to 0 if not set
        start_time = session.get('start_time', '00:00')  # Default to '00:00' if not set
        tasks = []
        total_duration = sleep_hours
=======
        # Retrieve task inputs from the form
        tasks = []
        index = 1
        while f'task{index}' in request.form:
            task_name = request.form.get(f'task{index}')
            task_duration = int(request.form.get(f'task{index}_duration'))
            if task_duration < 0:
                return "Durations must be positive.", 400
            tasks.append({"name": task_name, "duration": task_duration})
            index += 1
>>>>>>> Stashed changes

        # Loop through task inputs to collect names and durations
        for i in range(1, 10):  # Assuming a max of 9 tasks
            task_name = request.form.get(f'task{i}')
            task_duration = request.form.get(f'task{i}_duration')

<<<<<<< Updated upstream
            if task_name and task_duration:
                try:
                    task_duration = int(task_duration)
                    if task_duration < 0:
                        return "Durations must be positive.", 400
                    tasks.append((task_name, task_duration))
                    total_duration += task_duration
                except ValueError:
                    return "Invalid task duration. Please enter a valid number.", 400

        # Ensure the total time doesn't exceed 24 hours
        if total_duration > 24:
            return "The total duration of tasks and sleep cannot exceed 24 hours.", 400

        # Generate the schedule
        schedule = []
        start_hour, start_minute = map(int, start_time.split(':'))
        current_time = start_hour

        # Add sleep period to schedule
        sleep_end_hour = (current_time + sleep_hours) % 24
        schedule.append({
            "name": "Sleep",
            "start": f"{current_time:02}:{start_minute:02}",
            "end": f"{sleep_end_hour:02}:{start_minute:02}",
            "duration": sleep_hours
        })
        current_time = sleep_end_hour

        # Add tasks to schedule
        for task_name, task_duration in tasks:
            task_end_hour = (current_time + task_duration) % 24
            schedule.append({
                "name": task_name,
                "start": f"{current_time:02}:{start_minute:02}",
                "end": f"{task_end_hour:02}:{start_minute:02}",
                "duration": task_duration
            })
            current_time = task_end_hour
=======
        # Ensure the total time doesn't exceed 24 hours
        total_task_time = sum(task['duration'] for task in tasks)
        total_time = total_task_time + sleep_hours
        if total_time > 24:
            return "The total duration of tasks and sleep cannot exceed 24 hours.", 400

        # Generate the schedule and render it on the HTML page
        schedule = [
            {"name": "Sleep", "start": "00:00", "end": f"{sleep_hours:02}:00", "duration": sleep_hours}
        ]
        current_time = sleep_hours

        for task in tasks:
            start_time = current_time
            end_time = current_time + task['duration']
            schedule.append({"name": task['name'], "start": f"{start_time:02}:00", "end": f"{end_time:02}:00", "duration": task['duration']})
            current_time = end_time
>>>>>>> Stashed changes

        return render_template('schedule.html', schedule=schedule)

    except ValueError:
        return "Invalid input. Please enter valid task durations.", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

