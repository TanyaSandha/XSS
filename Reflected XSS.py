from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/addrec", methods = ['POST' , 'GET'])
def addrec():
    name = request.form['username']
    return '<h1>Hello {}</h1>'.format(name)
#    name.request.form["name_input"]
#   return render_template('index.html', name = name)

#@app.route("/result")
#def result():
#    return '<h1>Hello {}</h1>'.format(name)

if __name__ == '__main__':
    app.run(debug=True)