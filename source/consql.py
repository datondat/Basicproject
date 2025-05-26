import mysql.connector

class DatabaseConnector:
    def __init__(self, host='localhost', user='root', password='', database='basic_project'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
    def check(self,username,password):
        self.cursor.execute(
            "SELECT id FROM users WHERE logname = %s AND pass = %s",
            (username, password)
        )
        result = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result is not None

    def addus(self, fullname, gmail, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (fullname, mail, logname, pass) VALUES (%s, %s, %s, %s)",
                (fullname, gmail, username, password)
            )
            self.conn.commit()
            success = True
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            success = False
        finally:
            self.cursor.close()
            self.conn.close()
        return success