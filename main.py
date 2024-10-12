from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')  # Render the welcome page

@app.route('/next')
def next_page():
    return render_template('next_page.html')  # Render the next page (e.g., to-do list form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
