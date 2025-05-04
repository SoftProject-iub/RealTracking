import mysql

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def authenticate(self, username, password):
        """Authenticate user"""
        query = 'SELECT * FROM users WHERE username = %s AND password = %s'
        return self.db_manager.execute_query(query, (username, password), fetch_one=True)

    def create_user(self, username, email, password):
        """Create new user"""
        query = 'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)'
        try:
            self.db_manager.execute_query(query, (username, email, password), fetch_all=False)
            return True
        except mysql.connector.IntegrityError:
            return False

    def get_all_users(self):
        return self.db_manager.execute_query('SELECT * FROM users')

    def get_admin_stats(self):
        return {
            'buses': self.db_manager.execute_query('SELECT COUNT(id) FROM buses')[0]['COUNT(id)'],
            'users': self.db_manager.execute_query('SELECT COUNT(id) FROM users')[0]['COUNT(id)'],
            'routes': self.db_manager.execute_query('SELECT COUNT(id) FROM routes')[0]['COUNT(id)'],
            'feedback': self.db_manager.execute_query('SELECT COUNT(id) FROM feedback')[0]['COUNT(id)']
        }