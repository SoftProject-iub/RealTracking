class FeedbackManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_feedbacks(self):
        return self.db_manager.execute_query('SELECT * FROM feedback order by id desc')

    def create_feedback(self, name, email, message):
        try:
            self.db_manager.execute_query(
                'INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)',
                (name, email, message),
                fetch_all=False
            )
            return True
        except Exception:
            return False