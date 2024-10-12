from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


# Global progress value
progress_value = 0

@app.route('/')
def index():
    return render_template('progress.html')

@app.route('/progress')
def progress():
    return jsonify({"progress": progress_value})

@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['completed'] = not task['completed']
    return jsonify({'status': 'success', 'id': task_id, 'completed': task['completed']})

# New route to increase progress
@app.route('/increase_progress')
def increase_progress():
    global progress_value
    progress_value = min(100, progress_value + 33.3)  # Increase by 10%
    return jsonify({'status': 'success', 'progress': progress_value})

# New route to decrease progress
@app.route('/decrease_progress')
def decrease_progress():
    global progress_value
    progress_value = max(0, progress_value - 33.3)  # Decrease by 10%
    return jsonify({'status': 'success', 'progress': progress_value})

if __name__ == '__main__':
    app.run(debug=True)
