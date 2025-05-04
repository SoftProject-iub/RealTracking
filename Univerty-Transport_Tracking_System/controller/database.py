import mysql.connector

class DatabaseManager:
    """Handles all database operations"""
    def __init__(self, config):
        self.config = config

    def get_connection(self):
        """Establish database connection"""
        return mysql.connector.connect(**self.config)

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        """Generic method to execute queries"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = None
            return result
        finally:
            cursor.close()
            conn.close()