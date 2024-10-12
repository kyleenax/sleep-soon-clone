document.getElementById('schedule-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const tasks = document.getElementById('tasks').value.split(',');
    const sleepGoal = document.getElementById('sleep_goal').value;

    const response = await fetch('/schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tasks, sleep_goal: sleepGoal }),
    });

    const result = await response.json();
    document.getElementById('schedule-result').innerText = JSON.stringify(result);
});