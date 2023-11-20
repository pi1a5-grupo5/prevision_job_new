import psycopg2

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port="5432"
        )
        self.cursor = self.connection.cursor()

