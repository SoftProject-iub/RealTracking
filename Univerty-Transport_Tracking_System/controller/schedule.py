class ScheduleManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_schedules(self):
        return self.db_manager.execute_query('SELECT * FROM schedules')