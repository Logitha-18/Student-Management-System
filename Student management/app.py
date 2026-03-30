from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="school"
)
cursor = conn.cursor(dictionary=True)

# Home page - display all students
@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)

# Add new student
@app.route('/add', methods=['GET','POST'])

def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        cursor.execute("INSERT INTO students (name, age, email) VALUES (%s,%s,%s)", (name, age, email))
        conn.commit()
        return redirect('/')
    return render_template('add_student.html')

# Edit student
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_student(id):
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        cursor.execute("UPDATE students SET name=%s, age=%s, email=%s WHERE id=%s", (name, age, email, id))
        conn.commit()
        return redirect('/')
    return render_template('edit_student.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)