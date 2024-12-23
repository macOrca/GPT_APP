import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    # Create Problems table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Problems (
        problem_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        input_example TEXT NOT NULL,
        output_example TEXT NOT NULL,
        display_order INTEGER NOT NULL
    )''')

    # Create Submissions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Submissions (
        submission_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        problem_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        result TEXT,
        feedback TEXT,
        understanding REAL,
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(problem_id) REFERENCES Problems(problem_id)
    )''')

    conn.commit()
    conn.close()

def fetch_username(submission_user_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username FROM Users WHERE user_id = ?",
        (submission_user_id,)
    )
    username = cursor.fetchone()
    conn.close()
    return username

def fetch_problems():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Problems ORDER BY display_order")
    problems = cursor.fetchall()
    conn.close()
    return [
        {
            'problem_id': row[0],
            'title': row[1],
            'description': row[2],
            'input_example': row[3],
            'output_example': row[4],
            'display_order': row[5]
        }
        for row in problems
    ]

def add_problem(title, description, input_example, output_example, display_order):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Problems (title, description, input_example, output_example, display_order)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, description, input_example, output_example, display_order))
    conn.commit()
    conn.close()

def delete_problem(problem_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Problems WHERE problem_id = ?", (problem_id,))
    conn.commit()
    conn.close()


def fetch_submissions():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Submissions")
    submissions = cursor.fetchall()
    conn.close()
    return [
        {
            'submission_id': row[0],
            'user_id': row[1],
            'problem_id': row[2],
            'code': row[3],
            'result': row[4],
            'feedback': row[5],
            'understanding': row[6]
        }
        for row in submissions
    ]

def fetch_submissions_by_problem(problem_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT feedback FROM Submissions WHERE problem_id = ?",
        (problem_id,)
    )
    feedbacks = cursor.fetchall()
    conn.close()
    return [{'feedback': row[0]} for row in feedbacks]

def save_submission(user_id, problem_id, code, result, feedback):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Submissions (user_id, problem_id, code, result, feedback)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, problem_id, code, result, feedback))

    conn.commit()
    conn.close()
