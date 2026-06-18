import sqlite3
from pathlib import Path


class ChatHistoryDB:

    def __init__(self,db_path="data/chat_history.db",):

        Path("data").mkdir(
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False,
        )

        self.create_tables()

    # def create_table(self):

    #     cursor = self.conn.cursor()

    #     cursor.execute(
    #         """
    #         CREATE TABLE IF NOT EXISTS chats (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             role TEXT NOT NULL,
    #             content TEXT NOT NULL,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         )
    #         """
    #     )

    #     self.conn.commit()
    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            rating TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def create_session(self, title):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO sessions(title)
            VALUES(?)
            """,
            (title,)
        )

        self.conn.commit()

        return cursor.lastrowid
    
    def get_sessions(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT id,title
        FROM sessions
        ORDER BY id DESC
        """)

        return cursor.fetchall()



    # def save_message(self, role: str, content: str,):

    #     cursor = self.conn.cursor()

    #     cursor.execute(
    #         """
    #         INSERT INTO chats(
    #             role,
    #             content
    #         )
    #         VALUES (?, ?)
    #         """,
    #         (
    #             role,
    #             content,
    #         ),
    #     )

    #     self.conn.commit()

    def save_message(self, session_id, role, content):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages(
                session_id,
                role,
                content
            )
            VALUES(?,?,?)
            """,
            (
                session_id,
                role,
                content
            )
        )

        self.conn.commit()

        return cursor.lastrowid

    
    # def get_messages(self):

    #     cursor = self.conn.cursor()

    #     cursor.execute(
    #         """
    #         SELECT role, content
    #         FROM chats
    #         ORDER BY id ASC
    #         """
    #     )

    #     return cursor.fetchall()

    def get_session_messages(self, session_id):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT role,content
            FROM messages
            WHERE session_id=?
            ORDER BY id
            """,
            (session_id,)
        )

        return cursor.fetchall()
    

    def save_feedback(self, message_id, rating,):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO feedback(
                message_id,
                rating
            )
            VALUES(?,?)
            """,
            (
                message_id,
                rating,
            )
        )

        self.conn.commit()

    def update_session_title(self, session_id, title):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            UPDATE sessions
            SET title=?
            WHERE id=?
            """,
            (title, session_id)
        )

        self.conn.commit()

    def clear_session(self, session_id,):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM messages
            WHERE session_id = ?
            """,
            (session_id,)
        )

        self.conn.commit()  


    def delete_session(self, session_id,):

        cursor = self.conn.cursor()

        # Delete feedback first
        cursor.execute(
            """
            DELETE FROM feedback
            WHERE message_id IN (
                SELECT id
                FROM messages
                WHERE session_id = ?
            )
            """,
            (session_id,)
        )

        # Delete messages
        cursor.execute(
            """
            DELETE FROM messages
            WHERE session_id = ?
            """,
            (session_id,)
        )

        # Delete session
        cursor.execute(
            """
            DELETE FROM sessions
            WHERE id = ?
            """,
            (session_id,)
        )

        self.conn.commit() 


    def get_session_title(self, session_id,):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT title
            FROM sessions
            WHERE id = ?
            """,
            (session_id,),
        )

        result = cursor.fetchone()

        return result[0] if result else None
    




    def clear(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "DELETE FROM chats"
        )

        self.conn.commit()