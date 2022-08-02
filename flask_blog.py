from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

con = sqlite3.connect('database.db')

con.execute('CREATE TABLE IF NOT EXISTS login (username TEXT, password TEXT)')
print ("Table created successfully")
con.close()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/addrec", methods = ["POST"])
def addrec():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO login(username, password) VALUES(?,?)",(username, password))

            con.commit()
            msg = "Account successfully created"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg = msg)
            
    con.close()

@app.route('/list')
def list():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from login")
   
   rows = cur.fetchall()
   return render_template("list.html",rows = rows)
   
if __name__ == '__main__':
    app.run(debug=True)