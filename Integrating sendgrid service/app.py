from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
app = Flask(__name__)

app.secret_key='a'
SENDGRID_API_KEY = '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'
conn= ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kmr44787;PWD=I1l9dLWvqbFExm7p",'','')

@app.route('/')
def home():
    return render_template('login.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg= ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM members WHERE email=? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] =account['EMAIL']
            userid=  account['EMAIL']
            session['email'] =account['EMAIL']
            msg = 'Logged in successfully !'
            message = Mail(from_email='suga27102001@gmail.com',to_emails=email,subject='Sending mail using sendgrid',html_content='<strong>Logged in successfully</strong>')
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            print(sg)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return render_template('thankyou.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('login.html',msg=msg)
    
@app.route('/register', methods =['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM members WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        else:
            insert_sql = "INSERT INTO  members VALUES (?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, email)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
    
if __name__ == "__main__":
    app.run(debug=True)