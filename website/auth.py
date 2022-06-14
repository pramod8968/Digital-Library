from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import render_template, request,flash 
from . import db
import re
from .models import User, Department, Semester
auth = Blueprint('auth',__name__)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

@auth.route("/student_login",methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        susn = request.form.get('susn')
        student_password = request.form.get('student_lpassword')
        user = User.query.filter_by(usn=susn).first()
        if user:
            if(user.status=="Blocked"):
                flash('Sorry, You have been blocked. Please contact Library Admin', category='error')
                return render_template('student_login.html', user=current_user)  
            if check_password_hash(user.password,student_password):
                flash('Logged in Successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.student_home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('USN does not exist!', category='error')        
    return render_template('student_login.html', user=current_user)    


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
    return render_template('admin_login.html',user=current_user)    

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
    return render_template('teacher_login.html',user=current_user)   

@auth.route("/student_registration",methods=['GET','POST'])
def student_registration():
    departments = Department.query.all()
    semesters = Semester.query.all()
    pat = re.compile(r"1DS[0-9][0-9][A-Z][A-Z][0-9][0-9][0-9]")
    if request.method == 'POST':
        student_uname = request.form.get('sname')
        student_uemail = request.form.get('semail')
        student_upassword1 = request.form.get('spassword1')
        student_upassword2=request.form.get("spassword2")
        student_usn = request.form.get("susn")
        department = request.form.get('department')
        semester = request.form.get('semester') 

        user = User.query.filter_by(email=student_uemail).first()
        userusn = User.query.filter_by(usn=student_usn).first()
        if user:
            flash('Email already exists.',category='error')
        if userusn:
            flash('USN already exists',category='error')
        elif len(student_uemail)<4:
            flash('Email must be greater than 3 characters.',category='error')
        elif len(student_uname)<2:
            flash('First name must be greater than 1 characters.',category='error')
        elif student_upassword1 != student_upassword2:
            flash('Passwords don\'t match',category='error')
        elif len(student_upassword1)<7:
            flash('Password must be at least 7 characters length',category='error')
        else:
            if(pat.match(student_usn)):
                new_user = User(email=student_uemail, first_name=student_uname, password=generate_password_hash(student_upassword1, method='sha256'), urole = "student",is_active=True,usn=student_usn,department_id=department,semester_id=semester)
                db.session.add(new_user)
                db.session.commit()
                flash("Student Account Created", category='success')
                return render_template('student_login.html',user=current_user)
            else:
                flash('USN should be in Proper Format',category='error')
                return render_template('student_register.html', user=current_user) 
    return render_template('student_register.html', user=current_user, departments=departments, semesters=semesters) 

 
@auth.route("/teacher_registration",methods=['GET','POST'])
def teacher_registration():
    if request.method == 'POST':
        teacher_uname = request.form.get('tname')
        teacher_uemail = request.form.get('temail')
        teacher_upassword1 = request.form.get('tpassword1')
        teacher_upassword2=request.form.get("tpassword2")

        user = User.query.filter_by(email=teacher_uemail).first()

        if user:
            flash('Email already exists.',category='error')
        elif len(teacher_uemail)<4:
            flash('Email must be greater than 3 characters.',category='error')
        elif len(teacher_uname)<2:
            flash('First name must be greater than 1 characters.',category='error')
        elif teacher_upassword1 != teacher_upassword2:
            flash('Passwords don\'t match',category='error')
        elif len(teacher_upassword1)<7:
            flash('Password must be at least 7 characters length',category='error')
        
        else:
            new_user = User(email=teacher_uemail, first_name=teacher_uname, password=generate_password_hash(teacher_upassword1, method='sha256'), urole = "teacher",is_active=True,usn="Teacher")
            db.session.add(new_user)
            db.session.commit()
            flash("Teacher Account Created", category='success')
            return render_template('teacher_login.html',user=current_user)
            
    return render_template('teacher_register.html',user=current_user) 


@auth.route("/addanewadmin",methods=['GET','POST'])
def admin_registration():
    if request.method == 'POST':
        admin_uname = request.form.get('aname')
        admin_uemail = request.form.get('aemail')
        admin_upassword1 = request.form.get('apassword1')
        admin_upassword2=request.form.get("apassword2")

        user = User.query.filter_by(email=admin_uemail).first()

        if user:
            flash('Email already exists.',category='error')
        elif len(admin_uemail)<4:
            flash('Email must be greater than 3 characters.',category='error')
        elif len(admin_uname)<2:
            flash('First name must be greater than 1 characters.',category='error')
        elif admin_upassword1 != admin_upassword2:
            flash('Passwords don\'t match',category='error')
        elif len(admin_upassword1)<7:
            flash('Password must be at least 7 characters length',category='error')
        
        else:
            new_user = User(email=admin_uemail, first_name=admin_uname, password=generate_password_hash(admin_upassword1, method='sha256'), urole = "admin",is_active=True,usn="admin")
            db.session.add(new_user)
            db.session.commit()
            flash("Admin Account Created", category='success')
            return render_template('admin_login.html',user=current_user)
            
    return render_template('addmyadmin.html',user=current_user) 

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))