from flask import Flask, render_template, request, session, g, redirect, url_for
from flask_session import Session
import sqlite3
import os

con = sqlite3.connect('database.db')

con.execute('CREATE TABLE IF NOT EXISTS login (ID INTEGER, username TEXT, name TEXT, password TEXT, PRIMARY KEY("ID" AUTOINCREMENT))')
print ("Table created successfully")
con.close()

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/About')
def About():
    return render_template('index1.html')

@app.route("/addrec", methods = ["POST"])
def addrec():
    if request.method == 'POST':
        try:
            username = request.form['username']
            name = request.form['name']
            password = request.form['password']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO login(username, name, password) VALUES(?,?,?)",(username, name, password))

            con.commit()
            msg = "Account successfully created"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg = msg)
            
    con.close()

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if(request.method == "POST"):
        session.pop('username', None)
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM login WHERE username = '"+username+"'and password = '"+password+"'")
#        cur.execute("SELECT * FROM login WHERE username = '"+username+"'and name = '"+name+"'and password = '"+password+"'")
#        if request.form['password'] == password:
        if cur.fetchone():
            session['username'] = request.form['username']
            session['name'] = request.form['name']
            return '''<h1>Hi! {}</h1>'.format(name)'''
                                        
            
#            return redirect(url_for('result'))
    return render_template('login.html')
#        if not cur.fetchone():
#            msg = "login failed"
#            print(msg)
#            session['username'] = username
#            session['password'] = password
#        else:
#            msg = "Welcome {}".format(username)
#            print(msg)
#    return render_template("result1.html", msg = msg)

@app.route("/view", methods=['GET'])
def index():
    ID = request.args.get('ID')
#    ID = request.form['ID']
    db = sqlite3.connect("database.db")
    abc='select ID, username, password, name from login where ID='+ID
    cur=db.execute(abc)
    entry = cur.fetchall() 
    print(entry.index)
    return '<h1>hello {}</h1>'.format(entry)
	#return jsonify(entry)
#    return '''  <h1> ID|Username|Passowrd|Name </h1>  
#				<h1> {} | {} | {} | {}</h1>'''.format(entry[-1], entry[0], entry[1], entry[2])

@app.route('/result')
def result():
    if g.name:
        return render_template ('result1.html', name=session['name'])
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.name = None
    if 'name' in session:
        g.name = session['name']

@app.route('/dropsession')
def dropsession():
    session.pop['name', None]
    return render_template('login.html')

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