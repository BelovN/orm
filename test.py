import sqlite3

db = sqlite3.connect('example.db')
sql = db.cursor()


sql.execute('SELECT * FROM example;')
db.commit()

while a := sql.fetchone():
    print(a)
# a = sql.fetchone()
# print(a)
import pdb; pdb.set_trace()
