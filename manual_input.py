import sqlite3
from flask import Flask
app=Flask(__name__)
conn=sqlite3.connect("DriverInNeed")
cur=conn.cursor()
cur.execute("INSERT INTO admin (pos,adminName,adminPassword)VALUES ('admin','Turjo','admin')")
conn.commit()

if __name__=='__main__':
    app.run(debug=True)