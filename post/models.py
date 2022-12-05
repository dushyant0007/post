from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import sqlite3

with sqlite3.connect("database.db") as db:
        print(db.execute('select * from (user join post on user.google_id=post.google_id)').fetchall())
 


# class user(db.Model,UserMixin):
#     id = db.Column(db.Integer,primary_key=True)
#     email = db.Column(db.String(20),nullable=False,unique=True)
#     password = db.Column(db.String(80),nullable=False)



