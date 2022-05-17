from turtle import title
from website import create_app
from flask import render_template, request,flash 
from website.forms import Addbooks

import mysql.connector
import os  

app = create_app()
app.secret_key=os.urandom(24)

conn = mysql.connector.connect(host='localhost',user='root',password='Yanktron@123',database='flaskapp')
cursor = conn.cursor()

@app.route("/student_login",methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        student_email = request.form.get('student_lemail')
        student_password = request.form.get('student_lpassword')
        cursor.execute("select * from student where email like '{}' and password like '{}' ".format(student_email,student_password))
        users = cursor.fetchall()
    
        if len(users)>0:
            flash('Successfully Logged In :)',category='success')
            return render_template('student_home.html')
        else:
            flash('Incorrect Email or Password!!!',category='error')
    return render_template('student_login.html')    

@app.route("/admin_login",methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        admin_email = request.form.get('admin_lemail')
        admin_password = request.form.get('admin_lpassword')
        cursor.execute("select * from admin where email like '{}' and password like '{}' ".format(admin_email,admin_password))
        users = cursor.fetchall()
    
        if len(users)>0:
            flash('Successfully Logged In :)',category='success')
            return render_template('admin_home.html')
        else:
            flash('Incorrect Email or Password!!!',category='error')
    return render_template('admin_login.html')    

@app.route("/teacher_login",methods=['GET','POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_email = request.form.get('teacher_lemail')
        teacher_password = request.form.get('teacher_lpassword')
        cursor.execute("select * from teacher where email like '{}' and password like '{}' ".format(teacher_email,teacher_password))
        users = cursor.fetchall()
    
        if len(users)>0:
            flash('Successfully Logged In :)',category='success')
            return render_template('teacher_home.html')
        else:
            flash('Incorrect Email or Password!!!',category='error')
    return render_template('teacher_login.html')   

@app.route("/student_registration",methods=['GET','POST'])
def student_registration():
    if request.method == 'POST':
        student_uname = request.form.get('student_uname')
        student_uemail = request.form.get('student_uemail')
        student_upassword = request.form.get('student_upassword')
        if len(student_uname) < 2:
            flash('First Name must be greater than 1 character', category='error')
        elif len(student_uemail) < 4:
            flash('Email must be greater than 3 character', category='error')
        elif len(student_upassword) < 5:
            flash('Email must be greater than 4 character', category='error')  
        else:
            cursor.execute("insert into student (name,email,password) values('{}','{}','{}')".format(student_uname,student_uemail,student_upassword))
            conn.commit()
            flash('Accoutn created successfully!!',category='success')
            return render_template('student_login.html')
            
    return render_template('student_register.html') 

@app.route("/admin_registration",methods=['GET','POST'])
def admin_registration():
    if request.method == 'POST':
        admin_uname = request.form.get('admin_uname')
        admin_uemail = request.form.get('admin_uemail')
        admin_upassword = request.form.get('admin_upassword')
        if len(admin_uname) < 2:
            flash('First Name must be greater than 1 character', category='error')
        elif len(admin_uemail) < 4:
            flash('Email must be greater than 3 character', category='error')
        elif len(admin_upassword) < 5:
            flash('Email must be greater than 4 character', category='error')
        else:
            cursor.execute("insert into admin (name,email,password) values('{}','{}','{}')".format(admin_uname,admin_uemail,admin_upassword))
            conn.commit()
            flash('Accoutn created successfully!!',category='success')
            return render_template('admin_login.html')
    return render_template('admin_register.html') 

@app.route("/teacher_registration",methods=['GET','POST'])
def teacher_registration():
    if request.method == 'POST':
        teacher_uname = request.form.get('teacher_uname')
        teacher_uemail = request.form.get('teacher_uemail')
        teacher_upassword = request.form.get('teacher_upassword')
        if len(teacher_uname) < 2:
            flash('First Name must be greater than 1 character', category='error')
        elif len(teacher_uemail) < 4:
            flash('Email must be greater than 3 character', category='error')
        elif len(teacher_upassword) < 5:
            flash('Email must be greater than 4 character', category='error')
        else:
            cursor.execute("insert into teacher (name,email,password) values('{}','{}','{}')".format(teacher_uname,teacher_uemail,teacher_upassword))
            conn.commit()
            flash('Accoutn created successfully!!',category='success')
            return render_template('teacher_login.html')
    return render_template('teacher_register.html')


@app.route('/addbook',methods=['GET','POST'])
def addbook():
    form = Addbooks(request.form)
    return render_template('addbook.html',title="Add book Page",form = form)

#This is Darshan
#hello

if __name__=='__main__':
    app.run(debug="True")