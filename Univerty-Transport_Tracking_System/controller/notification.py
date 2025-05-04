class NotificationManager:
    """Handles notification operations"""
    def __init__(self, db_manager):
        self.db = db_manager

    def get_recent_notifications(self, limit=3):
        """Get recent notifications"""
        query = 'SELECT * FROM notifications ORDER BY created_at DESC LIMIT %s'
        return self.db.execute_query(query, (limit,))

    def create_notification(self, title, message, notification_type):
        """Create new notification"""
        query = 'INSERT INTO notifications (title, message, type) VALUES (%s, %s, %s)'
        self.db.execute_query(query, (title, message, notification_type), fetch_all=False)