from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', name='Baur')

@app.route('/greet')
def greet():
    if 'user' in request.args:
        usr = request.args['user']
        return render_template('greet.html', user = usr)
    else:
        return render_template('greet.html', user = 'Send your username with "user" parameter in query string')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        #Get the password and check it with database...
        #Assuming security checks are fine
        return render_template('secure.html', user = user_name)
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)