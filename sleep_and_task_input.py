# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate_schedule():
#     try:
#         task1_name = request.form['task1']
#         task1_duration = int(request.form['task1_duration'])
#         task2_name = request.form['task2']
#         task2_duration = int(request.form['task2_duration'])
#         task3_name = request.form['task3']
#         task3_duration = int(request.form['task3_duration'])
#        # sleep_hours = int(request.form['sleep'])

#         # Validate input
#         if task1_duration < 0 or task2_duration < 0 or task3_duration < 0: #or sleep_hours < 0:
#             return "Durations and sleep time must be positive integers.", 400

#         total_time = task1_duration + task2_duration + task3_duration #+ sleep_hours
#         if total_time > 24:
#             return "The total duration of tasks and sleep cannot exceed 24 hours.", 400

#         # Create the schedule
#         schedule = f"<strong>Schedule for the Day:</strong><br>"
#         current_time = 0  # Start at midnight (00:00)

#         # Sleep
#         # sleep_end_time = current_time + sleep_hours
#         # schedule += f"Sleep: 00:00 to {sleep_end_time:02}:00 ({sleep_hours} hours)<br>"
#         # current_time = sleep_end_time

#         # Task 1
#         task1_end_time = current_time + task1_duration
#         schedule += f"{task1_name}: {current_time:02}:00 to {task1_end_time:02}:00 ({task1_duration} hours)<br>"
#         current_time = task1_end_time

#         # Task 2
#         task2_end_time = current_time + task2_duration
#         schedule += f"{task2_name}: {current_time:02}:00 to {task2_end_time:02}:00 ({task2_duration} hours)<br>"
#         current_time = task2_end_time

#         # Task 3
#         task3_end_time = current_time + task3_duration
#         schedule += f"{task3_name}: {current_time:02}:00 to {task3_end_time:02}:00 ({task3_duration} hours)<br>"

#         return schedule

#     except ValueError:
#         return "Invalid input. Please enter valid task durations and sleep hours.", 400

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

@app.route('/')
def index():
    return render_template('sleep.html')

@app.route('/tasks', methods=['POST'])
def tasks():
    # Save the sleep hours input from the first page to session
    sleep_hours = request.form.get('sleep')
    if sleep_hours.isdigit() and int(sleep_hours) >= 0:
        session['sleep_hours'] = int(sleep_hours)
        return render_template('tasks.html')
    else:
        return "Please enter a valid sleep duration.", 400

@app.route('/generate', methods=['POST'])
def generate():
    # Save task inputs from the second page to session
    try:
        task1_name = request.form['task1']
        task1_duration = int(request.form['task1_duration'])
        task2_name = request.form['task2']
        task2_duration = int(request.form['task2_duration'])
        task3_name = request.form['task3']
        task3_duration = int(request.form['task3_duration'])
        sleep_hours = session.get('sleep_hours')

        # Validate task durations
        if task1_duration < 0 or task2_duration < 0 or task3_duration < 0:
            return "Durations must be positive.", 400

        total_time = task1_duration + task2_duration + task3_duration + sleep_hours
        if total_time > 24:
            return "The total duration of tasks and sleep cannot exceed 24 hours.", 400

        # Generate the schedule
        schedule = f"<strong>Schedule for the Day:</strong><br>"
        current_time = 0  # Start at midnight

        # Sleep
        sleep_end_time = current_time + sleep_hours
        schedule += f"Sleep: 00:00 to {sleep_end_time:02}:00 ({sleep_hours} hours)<br>"
        current_time = sleep_end_time

        # Task 1
        task1_end_time = current_time + task1_duration
        schedule += f"{task1_name}: {current_time:02}:00 to {task1_end_time:02}:00 ({task1_duration} hours)<br>"
        current_time = task1_end_time

        # Task 2
        task2_end_time = current_time + task2_duration
        schedule += f"{task2_name}: {current_time:02}:00 to {task2_end_time:02}:00 ({task2_duration} hours)<br>"
        current_time = task2_end_time

        # Task 3
        task3_end_time = current_time + task3_duration
        schedule += f"{task3_name}: {current_time:02}:00 to {task3_end_time:02}:00 ({task3_duration} hours)<br>"

        return schedule
    except ValueError:
        return "Invalid input. Please enter valid task durations.", 400

if __name__ == '__main__':
    app.run(debug=True)
