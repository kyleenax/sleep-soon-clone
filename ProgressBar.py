from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

# Simulated database of tasks
tasks = [
    {'id': 1, 'description': 'Task 1', 'completed': True},
    {'id': 2, 'description': 'Task 2', 'completed': False},
    {'id': 3, 'description': 'Task 3', 'completed': False}
]

@app.route('/')
def index():
    return render_template('progress.html', tasks=tasks)

@app.route('/progress')
def progress():
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task['completed'])
    progress = (completed_tasks / total_tasks) * 100
    return jsonify({"progress": progress})

@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['completed'] = not task['completed']
    return jsonify({'status': 'success', 'id': task_id, 'completed': task['completed']})

if __name__ == '__main__':
    app.run(debug=True)

