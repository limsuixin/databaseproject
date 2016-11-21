from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)
app.secret_key ="super secret key"

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/', methods =['POST'])
def index_post():
    conn=sqlite3.connect('bookstore.db')

    button= request.form['button']
    username = request.form['username']
    password = request.form['password']
    if button=="Sign up":    
        cursor = conn.execute("SELECT USERNAME from admin_acc")
        for row in cursor:
            if username == row[0]:
                flash("username already in use")
        cursor = conn.execute("SELECT USERNAME from user_acc")
        for row in cursor:
            if username == row[0]:
                flash("username already in use")
            
        if "admin" in username:
            conn.execute("INSERT INTO admin_acc VALUES(?, ?)",(username, password))
        else:
            conn.execute("INSERT INTO user_acc VALUES(?, ?)",(username, password))
        conn.commit()
        conn.close()
        flash("Account created")
        return render_template('main.html')

    else:
        cursor = conn.execute("SELECT * from user_acc ")
        for row in cursor:
            if (username == row[0] and password == row[1]):
                return redirect(url_for('acc',name=username))
            elif (username==row[0] and password!=row[1]):
                flash("Wrong password")
                render_template('main.html')
        
    
        flash("Username does not exist")
        return render_template('main.html')
            
            
@app.route('/search')
def advance():
    return render_template('advance.html')

@app.route('/<name>')
def acc(name):
    return render_template('user.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
