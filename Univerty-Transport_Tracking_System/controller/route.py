class RouteManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_routes(self):
        return self.db_manager.execute_query('SELECT * FROM routes')

    def add_route(self, name, stops):
        self.db_manager.execute_query(
            'INSERT INTO routes (name, stops) VALUES (%s, %s)',
            (name, stops),
            fetch_all=False
        )
        return True