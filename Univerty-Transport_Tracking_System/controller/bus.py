class BusManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_buses(self):
        return self.db_manager.execute_query('SELECT * FROM buses')

    def add_bus(self, name, route, status):
        self.db_manager.execute_query(
            'INSERT INTO buses (name, route, status) VALUES (%s, %s, %s)',
            (name, route, status),
            fetch_all=False
        )
        return True

    def get_map_stats(self):
        return {
            'buses': self.db_manager.execute_query('SELECT count(*) FROM buses')[0]['count(*)'],
            'routes': self.db_manager.execute_query('SELECT * FROM routes'),
            'active_bus': self.db_manager.execute_query("SELECT count(*) FROM buses WHERE status = 'Active'")[0]['count(*)'],
            'delayed': self.db_manager.execute_query("SELECT count(*) FROM buses WHERE status != 'Active'")[0]['count(*)']
        }