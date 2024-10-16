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
# @app.route('/tasks', methods=['POST'])
# def tasks():
#     sleep_hours = request.form.get('sleep')
#     start_time = request.form.get('start_time')

#     # Validate sleep hours (must be a non-negative number)
#     if sleep_hours and sleep_hours.isdigit() and int(sleep_hours) >= 0:
#         session['sleep_hours'] = int(sleep_hours)  # Store sleep hours in session

#         # Validate start time format (should be a valid time in HH:MM format)
#         if start_time:
#             try:
#                 hours, minutes = map(int, start_time.split(':'))
#                 if 0 <= hours < 24 and 0 <= minutes < 60:
#                     session['start_time'] = start_time  # Store start time in session
#                     return render_template('tasks.html')  # Render the task entry page
#                 else:
#                     return "Invalid start time. Please enter a valid time in HH:MM format.", 400
#             except ValueError:
#                 return "Invalid start time. Please enter a valid time in HH:MM format.", 400
#         else:
#             return "Start time is required.", 400
#     else:
#         return "Please enter a valid sleep duration.", 400
@app.route('/tasks', methods=['POST'])
def tasks():
    sleep_hours = request.form.get('sleep')
    start_time = request.form.get('start_time')

    # Validate sleep hours (must be between 6 and 12 hours)
    if sleep_hours and sleep_hours.isdigit():
        sleep_hours = int(sleep_hours)
        if 6 <= sleep_hours <= 12:
            session['sleep_hours'] = sleep_hours  # Store sleep hours in session

            # Validate start time format (should be a valid time in HH:MM format)
            if start_time:
                try:
                    hours, minutes = map(int, start_time.split(':'))
                    if 0 <= hours < 24 and 0 <= minutes < 60:
                        session['start_time'] = start_time  # Store start time in session
                        return render_template('tasks.html')  # Render the task entry page
                    else:
                        return render_template('sleep.html', message="Invalid start time. Please enter a valid time in HH:MM format.", sleep=sleep_hours, start_time=start_time)
                except ValueError:
                    return render_template('sleep.html', message="Invalid start time. Please enter a valid time in HH:MM format.", sleep=sleep_hours, start_time=start_time)
            else:
                return render_template('sleep.html', message="Start time is required.", sleep=sleep_hours, start_time=start_time)
        else:
            # Encourage a healthy sleep duration between 6 and 12 hours
            return render_template('sleep.html', message="Please enter a healthy sleep duration between 6 and 12 hours.", sleep=sleep_hours, start_time=start_time)
    else:
        return render_template('sleep.html', message="Please enter a valid sleep duration between 6 and 12 hours.", sleep=sleep_hours, start_time=start_time)

# @app.route('/tasks', methods=['POST']) KYLEENAAAASSS
# def tasks():
#     sleep_hours = request.form.get('sleep')  # Retrieve sleep hours from form
#     start_time = request.form.get('start_time')  # Retrieve start time from form

#     try:
#         # Convert sleep hours to a float to handle decimal entries
#         sleep_hours = float(sleep_hours)

#         # Check if sleep hours are within the valid range
#         if sleep_hours > 11:
#             return render_template('sleep.html', error="Sleep hours cannot exceed 12. Please enter a valid value.")
#         if sleep_hours < 7:
#             return render_template('sleep.html', error="Sleep hours cannot be below 6. Please enter a valid value.")

#         # Store valid sleep hours in the session
#         session['sleep_hours'] = sleep_hours

#         # Validate start time format
#         if start_time:
#             try:
#                 hours, minutes = map(int, start_time.split(':'))
#                 if 0 <= hours < 24 and 0 <= minutes < 60:
#                     session['start_time'] = start_time  # Store start time in session
#                     return redirect(url_for('task_entry'))  # Correctly redirect to the task entry page
#                 else:
#                     return render_template('sleep.html', error="Invalid start time. Please enter a valid time in HH:MM format.")
#             except ValueError:
#                 return render_template('sleep.html', error="Invalid start time. Please enter a valid time in HH:MM format.")
#         else:
#             return render_template('sleep.html', error="Start time is required.")

#     except ValueError:
#         return render_template('sleep.html', error="Invalid input for sleep hours. Please enter a number.")
import random
@app.route('/task_entry')
def task_entry():
    # Clear session values to reset inputs
    session.pop('sleep_hours', None)
    session.pop('start_time', None)
    return render_template('tasks.html')  # Ensure you create this template
@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    try:
        sleep_hours = session.get('sleep_hours', 0)  # Default to 0 if not set
        start_time = session.get('start_time', '00:00')  # Default to '00:00' if not set
        tasks = []
        total_duration = 0  # We calculate total duration of tasks first

        # List of mental health activities
        activities = ['meditate', 'yoga', 'walk', 'eat', 'drink water', 'nap', 'HIIT']

        # Collect task inputs
        for i in range(1, 10):  # Assuming a max of 9 tasks
            task_name = request.form.get(f'task{i}')
            task_duration = request.form.get(f'task{i}_duration')

            if task_name and task_duration:
                try:
                    task_duration = int(task_duration)
                    if task_duration < 0:
                        return render_template('tasks.html', error="Durations must be positive.", tasks=tasks, sleep_hours=sleep_hours, start_time=start_time), 400
                    tasks.append((task_name, task_duration))
                    total_duration += task_duration
                except ValueError:
                    return render_template('tasks.html', error="Invalid task duration. Please enter a valid number.", tasks=tasks, sleep_hours=sleep_hours, start_time=start_time), 400

        # Include breaks between tasks, but not after the last one
        total_break_time = (len(tasks) - 1) * 0.25  # 15-minute break between tasks
        total_duration += total_break_time

        # Check if the total task and break time exceeds the time before sleep (9:00 PM)
        max_available_time_for_tasks = (21 - int(start_time.split(':')[0]))  # Time until 9 PM

        if total_duration > max_available_time_for_tasks:
            error_message = "The total duration of tasks and breaks exceeds the time available before sleep at 9:00 PM."
            return render_template('tasks.html', error=error_message, tasks=tasks, sleep_hours=sleep_hours, start_time=start_time, show_remove=True), 400


        # Generate the schedule with tasks before sleep
        schedule = []
        start_hour, start_minute = map(int, start_time.split(':'))
        current_time_hour = start_hour
        current_time_minute = start_minute

        # Add tasks to the schedule, including 15-minute breaks with mental health suggestions
        for index, (task_name, task_duration) in enumerate(tasks):
            task_end_hour = (current_time_hour + task_duration) % 24
            schedule.append({
                "name": task_name,
                "start": f"{current_time_hour:02}:{current_time_minute:02}",
                "end": f"{task_end_hour:02}:{current_time_minute:02}",
                "duration": task_duration
            })
            current_time_hour = task_end_hour

            # Add 15-minute break, except for the last task
            if index < len(tasks) - 1:
                # current_time_minute += 15
                if current_time_minute >= 60:
                    current_time_hour = (current_time_hour + 1) % 24
                    current_time_minute %= 60

                # Choose a random mental health activity for the break
                activity = random.choice(activities)

                schedule.append({
                    "name": f"Break - {activity.capitalize()}",
                    "start": f"{current_time_hour:02}:{current_time_minute:02}",
                    "end": f"{current_time_hour:02}:{(current_time_minute + 15) % 60:02}",
                    "duration": 0.25
                })

                current_time_minute = (current_time_minute + 15) % 60
                if current_time_minute >= 60:
                    current_time_hour = (current_time_hour + 1) % 24
                    current_time_minute %= 60

        # Force sleep time between 9 PM and 11 PM
        sleep_start_hour = 21  # Sleep starts at 9 PM (21:00)
        sleep_end_hour = (sleep_start_hour + sleep_hours) % 24
        if sleep_end_hour > 23:
            return render_template('tasks.html', error="Sleep must end before 11:00 PM.", tasks=tasks, sleep_hours=sleep_hours, start_time=start_time), 400  # Sleep cannot extend beyond 11 PM

        schedule.append({
            "name": "Sleep",
            "start": f"{sleep_start_hour:02}:00",
            "end": f"{sleep_end_hour:02}:00",
            "duration": sleep_hours
        })

        return render_template('schedule.html', schedule=schedule)

    except ValueError:
        return render_template('tasks.html', error="Invalid input. Please enter valid task durations.", tasks=tasks, sleep_hours=sleep_hours, start_time=start_time), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
