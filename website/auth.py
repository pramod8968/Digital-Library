from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import render_template, request,flash 
import mysql.connector
from . import db
from .models import User
auth = Blueprint('auth',__name__)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user



conn = mysql.connector.connect(host='localhost',user='root',password='root',database='flaskapp')
cursor = conn.cursor()

@auth.route("/student_login",methods=['GET','POST'])
def student_login():
    
    if request.method == 'POST':
        student_email = request.form.get('student_lemail')
        student_password = request.form.get('student_lpassword')
        
        user = User.query.filter_by(email=student_email).first()

        if user:
            if check_password_hash(user.password,student_password):
                flash('Logged in Successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.student_home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email does not exist!', category='error')        
    return render_template('student_login.html')    

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route("/admin_login",methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        admin_email = request.form.get('admin_lemail')
        admin_password = request.form.get('admin_lpassword')
        
        user = User.query.filter_by(email=admin_email).first()
        if user:
            if check_password_hash(user.password,admin_password):
                flash('Logged in Successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.admin_home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email does not exist!', category='error')   
    return render_template('admin_login.html')    

@auth.route("/teacher_login",methods=['GET','POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_email = request.form.get('teacher_lemail')
        teacher_password = request.form.get('teacher_lpassword')
        user = User.query.filter_by(email=teacher_email).first()
        if user:
            if check_password_hash(user.password,teacher_password):
                flash('Logged in Successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.teacher_home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email does not exist!', category='error')   
    return render_template('teacher_login.html')   

@auth.route("/student_registration",methods=['GET','POST'])
def student_registration():
    if request.method == 'POST':
        student_uname = request.form.get('student_uname')
        student_uemail = request.form.get('student_uemail')
        student_upassword1 = request.form.get('student_upassword1')
        student_upassword2=request.form.get("student_upassword2")

        user = User.query.filter_by(email=student_uemail).first()

        if user:
            flash('Email already exists.',category='error')
        elif len(student_uemail)<4:
            flash('Email must be greater than 3 characters.',category='error')
        elif len(student_uname)<2:
            flash('First name must be greater than 1 characters.',category='error')
        elif student_upassword1 != student_upassword2:
            flash('Passwords don\'t match',category='error')
        elif len(student_upassword1)<7:
            flash('Password must be at least 7 characters length',category='error')
        
        else:
            new_user = User(email=student_uemail, first_name=student_uname, password=generate_password_hash(student_upassword1, method='sha256'), urole = "student",is_active=True)
            #new_user.roles.append(Role(name='student'))
    
            db.session.add(new_user)
            db.session.commit()

            #cursor.execute("insert into student (name,email,password) values('{}','{}','{}')".format(student_uname,student_uemail,student_upassword))
            #conn.commit()
            flash("Account Created", category='success')
            return render_template('student_login.html')
            
    return render_template('student_register.html') 

@auth.route("/admin_registration",methods=['GET','POST'])
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

@auth.route("/teacher_registration",methods=['GET','POST'])
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


 
