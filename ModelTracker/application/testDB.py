import sqlite3

connection = sqlite3.connect("data.sqlite")
cursor = connection.cursor()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())


query = "SELECT * FROM model_model"
rows = cursor.execute(query)

for row in rows:
    print(row)