import sqlite3
import json

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        understanding TEXT,
        misunderstanding TEXT
    )''')

    # Create Problems table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Problems (
        problem_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        input_example TEXT NOT NULL,
        output_example TEXT NOT NULL
    )''')

    # Create Submissions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Submissions (
        submission_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        problem_id INTEGER NOT NULL,
        code TEXT,
        output TEXT,
        answer_result TEXT,
        error_point TEXT,
        error_inference TEXT,
        problem_understanding TEXT,
        algorithm_design TEXT,
        code_implementation TEXT,
        execution_result TEXT,
        feedback TEXT,
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(problem_id) REFERENCES Problems(problem_id)
    )''')

    with open("users.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)

    for user in user_data:
        cursor.execute('''
        INSERT INTO Users (username, password, understanding, misunderstanding, interesting)
        VALUES (?, ?, ?, ?, ?)
        ''', (user['username'], user['password'], user['understanding'], user['misunderstanding'], user['interesting']))

    with open("problems.json", "r", encoding="utf-8") as f:
        problem_data = json.load(f)

    for problem in problem_data:
        cursor.execute('''
        INSERT INTO Problems (title, description, input_example, output_example)
        VALUES (?, ?, ?, ?)
        ''', (problem['title'], problem['description'], problem['input_example'], problem['output_example']))

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
    return username[0]

def fetch_problems():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Problems")
    problems = cursor.fetchall()
    conn.close()
    return [
        {
            'problem_id': row[0],
            'title': row[1],
            'description': row[2],
            'input_example': row[3],
            'output_example': row[4]
        }
        for row in problems
    ]

def add_problem(title, description, input_example, output_example):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Problems (title, description, input_example, output_example)
    VALUES (?, ?, ?, ?)
    ''', (title, description, input_example, output_example))
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
            'output': row[4],
            'answer_result': row[5],
            'error_point': row[6],
            'error_inference': row[7],
            'problem_understanding': row[8],
            'algorithm_design': row[9],
            'code_implementation': row[10],
            'execution_result': row[11],
            'feedback': row[12]
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

def save_submission(user_id, problem_id, code, output, feedback):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Submissions (user_id, problem_id, code, output, answer_result, error_point, error_inference, problem_understanding, algorithm_design, code_implementation, execution_result, feedback)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, problem_id, code, output, feedback.answer_result,feedback.error_point, feedback.error_inference, feedback.problem_understanding, feedback.algorithm_design, feedback.code_implementation,  feedback.execution_result,feedback.feedback))

    conn.commit()
    conn.close()

def fetch_user_profile(user_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT understanding, misunderstanding FROM Users WHERE user_id = ?",
        (user_id,)
    )
    user_profile = cursor.fetchone()
    conn.close()
    return user_profile

def save_user_profile(user_id, user_profile):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE Users SET understanding = ?, misunderstanding = ? WHERE user_id = ?;
    ''', (user_profile.understanding, user_profile.misunderstanding, user_id))
    conn.commit()
    conn.close()
