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
# @app.route('/generate_schedule', methods=['POST'])
# def generate_schedule():
#     try:
#         sleep_hours = session.get('sleep_hours', 0)  # Default to 0 if not set
#         start_time = session.get('start_time', '00:00')  # Default to '00:00' if not set
#         tasks = []
#         total_duration = sleep_hours

#         # Loop through task inputs to collect names and durations
#         for i in range(1, 10):  # Assuming a max of 9 tasks
#             task_name = request.form.get(f'task{i}')
#             task_duration = request.form.get(f'task{i}_duration')

#             if task_name and task_duration:
#                 try:
#                     task_duration = int(task_duration)
#                     if task_duration < 0:
#                         return "Durations must be positive.", 400
#                     tasks.append((task_name, task_duration))
#                     total_duration += task_duration
#                 except ValueError:
#                     return "Invalid task duration. Please enter a valid number.", 400

#         # Ensure the total time (tasks, sleep, and breaks) doesn't exceed 24 hours
#         total_break_time = (len(tasks) - 1) * 0.25  # 15-minute break between each task except the last one
#         total_duration += total_break_time

#         if total_duration > 24:
#             return "The total duration of tasks, sleep, and breaks cannot exceed 24 hours.", 400

#         # Generate the schedule
#         schedule = []
#         start_hour, start_minute = map(int, start_time.split(':'))
#         current_time_hour = start_hour
#         current_time_minute = start_minute

#         # Add sleep period to schedule
#         sleep_end_hour = (current_time_hour + sleep_hours) % 24
#         schedule.append({
#             "name": "Sleep",
#             "start": f"{current_time_hour:02}:{current_time_minute:02}",
#             "end": f"{sleep_end_hour:02}:{current_time_minute:02}",
#             "duration": sleep_hours
#         })
#         current_time_hour = sleep_end_hour

#         # Add tasks to schedule, including 15-minute breaks between tasks
#         for index, (task_name, task_duration) in enumerate(tasks):
#             task_end_hour = (current_time_hour + task_duration) % 24
#             schedule.append({
#                 "name": task_name,
#                 "start": f"{current_time_hour:02}:{current_time_minute:02}",
#                 "end": f"{task_end_hour:02}:{current_time_minute:02}",
#                 "duration": task_duration
#             })
#             current_time_hour = task_end_hour

#             # Add a 15-minute break, except for the last task
#             if index < len(tasks) - 1:
#                 # Add 15 minutes
#                 current_time_minute += 15
#                 if current_time_minute >= 60:
#                     current_time_hour = (current_time_hour + 1) % 24
#                     current_time_minute = current_time_minute % 60

#                 schedule.append({
#                     "name": "Break",
#                     "start": f"{current_time_hour:02}:{current_time_minute:02}",
#                     "end": f"{current_time_hour:02}:{(current_time_minute + 15) % 60:02}",
#                     "duration": 0.25
#                 })
#                 current_time_minute = (current_time_minute + 15) % 60
#                 if current_time_minute >= 60:
#                     current_time_hour = (current_time_hour + 1) % 24
#                     current_time_minute = current_time_minute % 60

#         return render_template('schedule.html', schedule=schedule)

#     except ValueError:
#         return "Invalid input. Please enter valid task durations.", 400
import random

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    try:
        sleep_hours = session.get('sleep_hours', 0)  # Default to 0 if not set
        start_time = session.get('start_time', '00:00')  # Default to '00:00' if not set
        tasks = []
        total_duration = sleep_hours

        # List of mental health activities
        activities = ['meditate', 'yoga', 'walk', 'eat', 'drink water', 'nap', 'HIIT']

        # Loop through task inputs to collect names and durations
        for i in range(1, 10):  # Assuming a max of 9 tasks
            task_name = request.form.get(f'task{i}')
            task_duration = request.form.get(f'task{i}_duration')

            if task_name and task_duration:
                try:
                    task_duration = int(task_duration)
                    if task_duration < 0:
                        return "Durations must be positive.", 400
                    tasks.append((task_name, task_duration))
                    total_duration += task_duration
                except ValueError:
                    return "Invalid task duration. Please enter a valid number.", 400

        # Ensure the total time (tasks, sleep, and breaks) doesn't exceed 24 hours
        total_break_time = (len(tasks) - 1) * 0.25  # 15-minute break between each task except the last one
        total_duration += total_break_time

        if total_duration > 24:
            return "The total duration of tasks, sleep, and breaks cannot exceed 24 hours.", 400

        # Generate the schedule
        schedule = []
        start_hour, start_minute = map(int, start_time.split(':'))
        current_time_hour = start_hour
        current_time_minute = start_minute

        # Add sleep period to schedule
        sleep_end_hour = (current_time_hour + sleep_hours) % 24
        schedule.append({
            "name": "Sleep",
            "start": f"{current_time_hour:02}:{current_time_minute:02}",
            "end": f"{sleep_end_hour:02}:{current_time_minute:02}",
            "duration": sleep_hours
        })
        current_time_hour = sleep_end_hour

        # Add tasks to schedule, including 15-minute breaks with mental health suggestions
        for index, (task_name, task_duration) in enumerate(tasks):
            task_end_hour = (current_time_hour + task_duration) % 24
            schedule.append({
                "name": task_name,
                "start": f"{current_time_hour:02}:{current_time_minute:02}",
                "end": f"{task_end_hour:02}:{current_time_minute:02}",
                "duration": task_duration
            })
            current_time_hour = task_end_hour

            # Add a 15-minute break with a random mental health suggestion, except for the last task
            if index < len(tasks) - 1:


                if current_time_minute >= 60:
                    current_time_hour = (current_time_hour + 1) % 24
                    current_time_minute = current_time_minute % 60

                # Choose a random activity
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
                    current_time_minute = current_time_minute % 60

        return render_template('schedule.html', schedule=schedule)

    except ValueError:
        return "Invalid input. Please enter valid task durations.", 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
