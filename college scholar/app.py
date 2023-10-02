from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key='637465'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dharun@0501'
app.config['MYSQL_DB'] = 'mini'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

# Registration route

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password or not email:
            flash('Please fill out the form!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid Email Address', 'error')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                           (username, password, email))
            mysql.connection.commit()
            cursor.close()
            flash('Registration successful', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user['password'] == password:
            session['loggedin'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('showform'))
        else:
            flash('Incorrect username or password', 'error')

    return render_template('login.html')

# admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password,))
        admin = cursor.fetchone()
        cursor.close()

        if admin and admin['password'] == password:
            session['loggedin'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('viewrecord'))
        else:
            flash('Incorrect username or password', 'error')
    return render_template('admin.html')

@app.route('/form',methods=["GET","POST"])
# form
def showform():
    if 'loggedin' in session:
            if request.method=='POST':
                sname=request.form['sname']
                semail=request.form['semail']
                sdob=request.form['sdob']
                sid=request.form['sid']
                spercentage=request.form['spercentage']
                sphone=request.form['sphone']
                cursor=mysql.connection.cursor()
                cursor.execute("INSERT INTO avengers(sname,semail,sdob,sid,spercentage,sphone) VALUES (%s, %s, %s,%s,%s,%s)",(sname, semail, sdob,sid,spercentage,sphone))
                mysql.connection.commit()
                cursor.close()
            return render_template('form.html', username=session['username'])
    else:
        #flash('You need to login first', 'error')
        return redirect(url_for('login'))

#admin data view
@app.route('/datalist',methods=['POST','GET'])
def viewrecord():
    if 'loggedin' in session:
        if request.method=='GET':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM avengers")
            avengers = cursor.fetchall()
            avengers_record= [{'id':row[0],'sname':row[1], 'semail':row[2],'sdob':row[3], 'sid':row[4], 'spercentage':row[5],'sphone':row[6]}for row in avengers]
            cursor.close()
        return render_template('studentdata.html',avengers = avengers_record)
    else:
        return redirect(url_for('admin'))



'''
def studdata():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM data')
    form= cursor.fetchall()
    studentdata =[{'name':row[1],''}]
    cursor.close()
    return render_template('studentdata.html',data=studentdata)
    '''


'''
# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        #flash('You need to login first', 'error')
        return redirect(url_for('login'))
'''


# Logout route
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    #flash('You have been logged out', 'success')
    return render_template('home.html')

'''
@app.route('/delete/<int:id>', methods = ['GET','POST'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM avengers WHERE id=%s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('delete',['id']))
    '''
    

''' chat gpt
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if 'loggedin' in session:
        if session.get('role') == 'admin':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("DELETE FROM avengers WHERE id = %s", (id,))
            mysql.connection.commit()
            cursor.close()
            flash('Record deleted successfully', 'success')
        else:
            flash('You do not have permission to delete records', 'error')
        return redirect(url_for('viewrecord'))  # Redirect to the viewrecord page
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))
'''


if __name__ == '__main__':
    app.run(debug=True)
