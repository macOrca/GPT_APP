import sqlite3
import pandas as pd

# データベース接続関数
def get_connection():
    conn = sqlite3.connect("student_model.db")
    return conn

# データベースとテーブルを初期化する関数
def initialize_database():
    # データベースに接続
    conn = sqlite3.connect("student_model.db")
    cursor = conn.cursor()

    # テーブルを作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,         -- 学習者の識別ID
            name TEXT NOT NULL,             -- 学習者の名前
            password TEXT NOT NULL,         -- パスワード
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learner_model (
            user_id INTEGER PRIMARY KEY,    -- 学習者の識別ID
            concepts_used TEXT,             -- 使用された概念（カンマ区切り）
            code_length INTEGER,            -- コードの行数
            skill_level TEXT,               -- 推定されたスキルレベル
            syntax_valid INTEGER,           -- 構文が正しいか (1: 正しい, 0: エラーあり)
            errors TEXT,                    -- エラーまたは改善点（セミコロン区切り）
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
