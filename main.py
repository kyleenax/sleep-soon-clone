from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML template

@app.route("/schedule", methods=['POST'])
def schedule():
    data = request.get_json()
    tasks = data.get('tasks', [])
    sleep_goal = data.get('sleep_goal', 8)
    schedule = optimize_schedule(tasks, sleep_goal)
    return jsonify(schedule)

def optimize_schedule(tasks, sleep_goal):
    # Placeholder for optimization logic
    return {
        "tasks": tasks,
        "sleep_goal": sleep_goal,
        "optimized": True
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
