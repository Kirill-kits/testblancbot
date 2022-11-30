import sqlite3

class Database():
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        result = self.connection.execute(f'SELECT * FROM users WHERE user_id = {user_id}').fetchall()
        return bool(len(result))

    def set_email(self, user_id, email):
        with self.connection:
            return self.cursor.execute("UPDATE users SET email = ? WHERE user_id = ?", (email, user_id,))

    def get_email(self, user_id):
        result = self.connection.execute(f'SELECT email FROM users WHERE user_id ={user_id}').fetchone()
        return result[0]
    
    def set_logpass(self, user_id, logpass):
        with self.connection:
            return self.cursor.execute("UPDATE users SET logpass = ? WHERE user_id = ?", (logpass, user_id,))

    def get_logpass(self, user_id):
        result = self.connection.execute(f'SELECT logpass FROM users WHERE user_id ={user_id}').fetchone()
        return result[0]

    def get_passin(self, user_id):
        result = self.connection.execute(f"SELECT passin FROM users WHERE user_id ='{user_id}'").fetchone()
        return result[0]
    
    def set_passin(self, user_id, passin):
        with self.connection:
            return self.cursor.execute("UPDATE users SET passin = ? WHERE user_id = ?", (passin, user_id,))
    
    def get_email_saved(self, user_id):
        result = self.connection.execute(f"SELECT email_saved FROM users WHERE user_id ='{user_id}'").fetchone()
        return result[0]
    
    def set_email_saved(self, user_id, email_saved):
        with self.connection:
            return self.cursor.execute("UPDATE users SET email_saved = ? WHERE user_id = ?", (email_saved, user_id,))
               