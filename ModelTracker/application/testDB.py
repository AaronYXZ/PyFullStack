import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
# https://stackoverflow.com/questions/82875/how-to-list-the-tables-in-a-sqlite-database-file-that-was-opened-with-attach
# https://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api
query = "SELECT * FROM model_info"
rows = cursor.execute(query)

for row in rows:
    print(row)

query = "SELECT * FROM train_result"
rows = cursor.execute(query)
print(cursor.fetchall())

query = "SELECT * FROM test_result"
rows = cursor.execute(query)
print(cursor.fetchall())