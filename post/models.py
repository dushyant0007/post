import sqlite3

with sqlite3.connect('temp.db') as temp:
        # with sqlite3.connect('database.db') as db:
                # db.execute('create table one (Emp_No int , Name text , Department TEXT,Designation TEXT)')
        x = temp.execute('select * from one')
        print(x)
