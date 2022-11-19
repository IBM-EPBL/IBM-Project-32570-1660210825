from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import smtplib
from prettytable import from_db_cursor

app = Flask(__name__)
app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kmr44787;PWD=s23SOOv7QL60Zm1o", '', '')


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            ser = smtplib.SMTP('smtp.gmail.com', 587)
            ser.starttls()
            ser.login('suga27102001@gmail.com', '****************')
            ser.sendmail('suga27102001@gmail.com', username,
                         'Congratulations !!! Logged in successfully')
            print(session['username'])
            return render_template('dashboard.html', msg=username)
        else:
            msg = 'Incorrect username/password !'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            ser = smtplib.SMTP('smtp.gmail.com', 587)
            ser.starttls()
            ser.login('suga27102001@gmail.com', '****************')
            ser.sendmail('suga27102001@gmail.com', username,
                         'Congratulations !!! Registered successfully')
            return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/dashView')
def dashView():
    msg = ''
    itemname = []
    quantity = []
    stmt = ibm_db.exec_immediate(conn, "select * from stock")
    while ibm_db.fetch_row(stmt) != False:
        itemname.append(ibm_db.result(stmt, 0))
        quantity.append(ibm_db.result(stmt, 1))
        print("ItemName is : ", ibm_db.result(stmt, 0),
              " Quantity : ", ibm_db.result(stmt, 1))
    return render_template('inventory.html', msg=msg, itemname=itemname, quantity=quantity, lenin=len(itemname), lenqty=len(quantity))


@app.route('/inventory')
def inventory():
    return render_template('dashboard.html')


@app.route('/dashAdd', methods=['GET', 'POST'])
def dashAdd():
    msg = ''
    if request.method == 'POST':
        itemname = request.form['itemname']
        quantity = request.form['quantity']
        insert_sql = "INSERT INTO stock VALUES (?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, itemname)
        ibm_db.bind_param(prep_stmt, 2, quantity)
        ibm_db.execute(prep_stmt)
        msg = 'Stock added!'
        return render_template('dashboard.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('dashboard.html', msg=msg)


@app.route('/dashUpdate', methods=['GET', 'POST'])
def dashUpdate():
    msg = ''
    if request.method == 'POST':
        itemname = request.form['itemname']
        quantity = request.form['quantity']
        update = request.form['update']
        sql = "select quantity from stock where itemname=?"
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(prep_stmt, 1, itemname)
        ibm_db.execute(prep_stmt)
        quan = ibm_db.fetch_assoc(prep_stmt)
        dk = ''
        if quan:
            for i in quan:
                dk = quan[i]
            if (update == 'restock'):
                result = int(dk)+int(quantity)
            if (update == 'halt'):
                result = int(dk)-int(quantity)
        if result < 0:
            result = 0
            ser = smtplib.SMTP('smtp.gmail.com', 587)
            ser.starttls()
            ser.login('suga27102001@gmail.com', '****************')
            ser.sendmail('suga27102001@gmail.com',
                         session['username'], 'Just a reminder, your stocks were drained, so restock them.')
            print('mail sent')
            print(session['username'])
        sql1 = "UPDATE stock SET quantity=? WHERE itemname=?"
        prep_stmt1 = ibm_db.prepare(conn, sql1)
        ibm_db.bind_param(prep_stmt1, 1, result)
        ibm_db.bind_param(prep_stmt1, 2, itemname)
        ibm_db.execute(prep_stmt1)
        return render_template('dashboard.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('dashboard.html', msg=msg)


@app.route('/dashDelete', methods=['GET', 'POST'])
def dashDelete():
    msg = ''
    if request.method == 'POST':
        itemname = request.form['itemname']
        delete_sql = "DELETE FROM stock WHERE itemname = ?;"
        prep_stmt = ibm_db.prepare(conn, delete_sql)
        ibm_db.bind_param(prep_stmt, 1, itemname)
        ibm_db.execute(prep_stmt)
        msg = 'Stock deleted!'
        return render_template('dashboard.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('dashboard.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
