from flask import Flask, render_template, redirect, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key in production

# Dummy database for users and courses (for demonstration)
users = {
    'user1': {
        'username': 'user1',
        'password': generate_password_hash('password1'),  # hashed password
        'courses': []
    }
}

courses = []

# Routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'Username already exists!'
        users[username] = {
            'username': username,
            'password': generate_password_hash(password),
            'courses': []
        }
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect(url_for('my_courses'))
        return 'Invalid username or password!'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_description = request.form['course_description']
        courses.append({
            'course_name': course_name,
            'course_description': course_description,
            'instructor': session['username']
        })
        users[session['username']]['courses'].append(course_name)
        return redirect(url_for('my_courses'))
    return render_template('create_course.html')

@app.route('/my_courses')
def my_courses():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_courses = [course for course in courses if course['instructor'] == session['username']]
    return render_template('my_courses.html', courses=user_courses)

@app.route('/course/<string:course_name>')
def course(course_name):
    course = next((c for c in courses if c['course_name'] == course_name), None)
    if not course:
        return 'Course not found!'
    return render_template('course.html', course=course)

if __name__ == '__main__':
    app.run(debug=True)
