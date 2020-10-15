from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'This is home page for "/" path. <h1>Welcome to Clarusway Hands-on</h>'

@app.route('/about')
def about():
    return '<h1>This is my about page...</h1>'

@app.route('/error')
def error():
    return '<h1>Either you encouterred an error <p>or <p>you are not authorized.</h1>'

@app.route('/hello')
def hello():
    return '<h1>Hello from Baur!</h1>'

@app.route('/admin', methods=['GET']) #by default GET method, multiple methods can be added
def admin():
    authorized = False
    if authorized:
        return '<h1>This is the admin page.... <p>only admins can see this page!</p></h1>'
    else:
        return redirect(url_for('error'))

@app.route('/<name>')
def greet(name):
    return render_template('greet.html', person=name)
    #greet_format=f"""
    #<!DOCTYPE html>
    #<html>
    #<head>
    #    <title>Greeting Page</title>
    #</head>
    #<body>
    #    <h1>Hello, { name }!</h1>
    #    <h1>Welcome to my Greeting Page</h1>
    #</body>
    #</html>
    #"""
    #return greet_format

@app.route('/greet-admin')
def greet_admin():
    return redirect(url_for('greet', name = 'Master Admin!!!'))

@app.route('/list10')
def list10():
    return render_template('list10.html')

@app.route('/evens')
def evens():
    return render_template('evens.html')



if __name__ == "__main__":
    app.run(host='localhost', port = 5000, debug=True)