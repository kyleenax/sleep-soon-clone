from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/schedule", methods=['POST'])
def schedule():
    data = request.get_json()
    tasks = data.get('tasks', [])
    sleep_goal = data.get('sleep_goal', 8)
    # Placeholder for scheduling logic
    schedule = optimize_schedule(tasks, sleep_goal)
    return jsonify(schedule)


def optimize_schedule(tasks, sleep_goal):
    # Placeholder for optimization logic
    # This function should return an optimized schedule
    return {
        "tasks": tasks,
        "sleep_goal": sleep_goal,
        "optimized": True
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')








from datetime import datetime, timedelta

def optimize_schedule(tasks, sleep_goal):
    # Assuming tasks is a list of dictionaries with 'name', 'duration', and 'deadline'
    # Example task: {'name': 'Task 1', 'duration': 2, 'deadline': '2024-10-12 18:00'}

    # Convert deadline strings to datetime objects for easier manipulation
    for task in tasks:
        task['deadline'] = datetime.strptime(task['deadline'], '%Y-%m-%d %H:%M')

    # Sort tasks by deadline
    tasks.sort(key=lambda x: x['deadline'])

    # Initialize the schedule dictionary
    schedule = {'tasks': [], 'sleep_blocks': []}

    # Define the start of the scheduling period (e.g., today at 6 AM)
    start_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=1)  # 24-hour scheduling window

    # Reserve a sleep block (try to schedule sleep from 10 PM to 6 AM)
    sleep_start = start_time.replace(hour=22, minute=0)
    sleep_end = sleep_start + timedelta(hours=sleep_goal)

    current_time = start_time

    # Schedule tasks greedily based on their deadlines
    for task in tasks:
        task_duration = timedelta(hours=task['duration'])

        # Check if the task can be completed before its deadline and without overlapping sleep
        if current_time + task_duration <= task['deadline'] and (current_time + task_duration <= sleep_start or current_time >= sleep_end):
            schedule['tasks'].append({'name': task['name'], 'start': current_time, 'end': current_time + task_duration})
            current_time += task_duration
        elif current_time < sleep_start and current_time + task_duration > sleep_start:
            # If task overlaps with sleep, move current time to after sleep
            current_time = sleep_end
            if current_time + task_duration <= task['deadline']:
                schedule['tasks'].append({'name': task['name'], 'start': current_time, 'end': current_time + task_duration})
                current_time += task_duration

    # Add sleep block to the schedule
    schedule['sleep_blocks'].append({'start': sleep_start, 'end': sleep_end})

    return schedule

# Example usage
tasks = [
    {'name': 'Task 1', 'duration': 2, 'deadline': '2024-10-12 18:00'},
    {'name': 'Task 2', 'duration': 1.5, 'deadline': '2024-10-12 12:00'},
    {'name': 'Task 3', 'duration': 3, 'deadline': '2024-10-12 20:00'}
]

sleep_goal = 8
optimized_schedule = optimize_schedule(tasks, sleep_goal)
print(optimized_schedule)
