import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


create_table_query = "Create table if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table_query)


create_table_query = "Create table if not exists items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table_query)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()
connection.close()