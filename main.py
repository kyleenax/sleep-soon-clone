# import tkinter as tk
# from tkinter import messagebox
# from datetime import datetime, timedelta

# # Function to generate optimized schedule
# def generate_schedule():
#     try:
#         task1_name = task1_entry.get()
#         task1_duration = int(task1_duration_entry.get())
#         task2_name = task2_entry.get()
#         task2_duration = int(task2_duration_entry.get())
#         task3_name = task3_entry.get()
#         task3_duration = int(task3_duration_entry.get())
#         sleep_hours = int(sleep_entry.get())

#         # Validate inputs: No negative values allowed
#         if task1_duration < 0 or task2_duration < 0 or task3_duration < 0 or sleep_hours < 0:
#             raise ValueError("Durations and sleep time must be positive integers.")

#         total_time = task1_duration + task2_duration + task3_duration + sleep_hours

#         # Ensure the total time (tasks + sleep) does not exceed 24 hours
#         if total_time > 24:
#             raise ValueError("The total duration of tasks and sleep cannot exceed 24 hours.")

#         # Build the schedule
#         now = datetime.now().replace(minute=0, second=0, microsecond=0)
#         schedule = f"Schedule for the Day:\n"

#         sleep_start_time = now
#         sleep_end_time = sleep_start_time + timedelta(hours=sleep_hours)
#         schedule += f"Sleep: {sleep_start_time.strftime('%H:%M')} to {sleep_end_time.strftime('%H:%M')} ({sleep_hours} hours)\n"

#         task_start_time = sleep_end_time

#         task1_end_time = task_start_time + timedelta(hours=task1_duration)
#         schedule += f"{task1_name}: {task_start_time.strftime('%H:%M')} to {task1_end_time.strftime('%H:%M')} ({task1_duration} hours)\n"
#         task_start_time = task1_end_time

#         task2_end_time = task_start_time + timedelta(hours=task2_duration)
#         schedule += f"{task2_name}: {task_start_time.strftime('%H:%M')} to {task2_end_time.strftime('%H:%M')} ({task2_duration} hours)\n"
#         task_start_time = task2_end_time

#         task3_end_time = task_start_time + timedelta(hours=task3_duration)
#         schedule += f"{task3_name}: {task_start_time.strftime('%H:%M')} to {task3_end_time.strftime('%H:%M')} ({task3_duration} hours)\n"

#         # Show the generated schedule
#         messagebox.showinfo("Optimized Schedule", schedule)

#     except ValueError as ve:
#         messagebox.showerror("Input Error", str(ve))

# # Create the GUI window
# root = tk.Tk()
# root.title("Daily Schedule Optimizer")

# # Task 1 inputs
# task1_label = tk.Label(root, text="Task 1:")
# task1_label.grid(row=0, column=0)
# task1_entry = tk.Entry(root)
# task1_entry.grid(row=0, column=1)

# task1_duration_label = tk.Label(root, text="Duration (hours):")
# task1_duration_label.grid(row=0, column=2)
# task1_duration_entry = tk.Entry(root)
# task1_duration_entry.grid(row=0, column=3)

# # Task 2 inputs
# task2_label = tk.Label(root, text="Task 2:")
# task2_label.grid(row=1, column=0)
# task2_entry = tk.Entry(root)
# task2_entry.grid(row=1, column=1)

# task2_duration_label = tk.Label(root, text="Duration (hours):")
# task2_duration_label.grid(row=1, column=2)
# task2_duration_entry = tk.Entry(root)
# task2_duration_entry.grid(row=1, column=3)

# # Task 3 inputs
# task3_label = tk.Label(root, text="Task 3:")
# task3_label.grid(row=2, column=0)
# task3_entry = tk.Entry(root)
# task3_entry.grid(row=2, column=1)

# task3_duration_label = tk.Label(root, text="Duration (hours):")
# task3_duration_label.grid(row=2, column=2)
# task3_duration_entry = tk.Entry(root)
# task3_duration_entry.grid(row=2, column=3)

# # Sleep input
# sleep_label = tk.Label(root, text="Desired Sleep (hours):")
# sleep_label.grid(row=3, column=0)
# sleep_entry = tk.Entry(root)
# sleep_entry.grid(row=3, column=1)

# # Generate button
# generate_button = tk.Button(root, text="Generate Schedule", command=generate_schedule)
# generate_button.grid(row=4, columnspan=4)

# # Run the application
# root.mainloop()

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_schedule():
    try:
        task1_name = request.form['task1']
        task1_duration = int(request.form['task1_duration'])
        task2_name = request.form['task2']
        task2_duration = int(request.form['task2_duration'])
        task3_name = request.form['task3']
        task3_duration = int(request.form['task3_duration'])
        sleep_hours = int(request.form['sleep'])

        # Validate input
        if task1_duration < 0 or task2_duration < 0 or task3_duration < 0 or sleep_hours < 0:
            return "Durations and sleep time must be positive integers.", 400

        total_time = task1_duration + task2_duration + task3_duration + sleep_hours
        if total_time > 24:
            return "The total duration of tasks and sleep cannot exceed 24 hours.", 400

        # Create the schedule
        schedule = f"<strong>Schedule for the Day:</strong><br>"
        current_time = 0  # Start at midnight (00:00)

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
        return "Invalid input. Please enter valid task durations and sleep hours.", 400

if __name__ == '__main__':
    app.run(debug=True)
