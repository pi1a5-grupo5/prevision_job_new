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


db = DatabaseConnection(
    host="carllet-dev.cygduzvreboa.us-east-2.rds.amazonaws.com",
    database="development",
    user="postgres",
    password="0*6Q8uJxI95OSyc$"
)

# db.cursor.execute('SELECT * FROM usuarios')
# rows = db.cursor.fetchall()
# for row in rows:
#     print(row)

print(db.connection.info)
print(db.connection.status)


db.cursor.close()
db.connection.close()



# import psycopg2

# class DatabaseConnection:
#     def __init__(self, host, database, user, password):
#         self.connection = psycopg2.connect(
#             host="carllet-dev.cygduzvreboa.us-east-2.rds.amazonaws.com",
#             database="development",
#             user="postgres",
#             password="0*6Q8uJxI95OSyc$",
#             port = "5432"
#         )

# # conn = psycopg2.connect(database = "development",
# #                         host = "carllet-dev.cygduzvreboa.us-east-2.rds.amazonaws.com",
# #                         user = "postgres",
# #                         password = "0*6Q8uJxI95OSyc$",
# #                         port = "5432")


# cur = DatabaseConnection.cursor()

# cur.execute('SELECT * FROM "Ganho"')
# for row in cur:
#     print(row)

# DatabaseConnection.commit()

# print(DatabaseConnection.info)
# print(DatabaseConnection.status)

# DatabaseConnection.close()