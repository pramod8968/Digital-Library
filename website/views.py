
from unicodedata import category
from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, current_user
from flask import flash
from flask import url_for
from . import db


from website.forms import Addbooks
from .models import Department,Semester

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home_page.html", user=current_user)

@views.route('/student_home')
@login_required
def student_home():
    return render_template("student_home.html", user=current_user)

@views.route('/admin_home')
@login_required
def admin_home():
    return render_template("admin_home.html", user=current_user)

@views.route('/teacher_home')
@login_required
def teacher_home():
    return render_template("teacher_home.html", user=current_user)

@views.route('/aboutUs')
def about_us():
    return render_template("About_Us.html", user=current_user)


@views.route('/adddepartment', methods=['GET','POST'])
def adddepartment():
    if request.method == "POST":
        getdepartment = request.form.get('department')
        department = Department(name=getdepartment)
        db.session.add(department)
        flash(f'The Department {getdepartment} was added to your database','success')
        db.session.commit()
        return redirect(url_for('views.adddepartment'))
        
    return render_template('add_department.html', departments='departments', user=current_user)


@views.route('/addsemester', methods=['GET','POST'])
def addsemester():
    if request.method == "POST":
        getsemester = request.form.get('semester')
        semester = Semester(name=getsemester)
        db.session.add(semester)
        flash(f'The Semester {getsemester} was added to your database','success')
        db.session.commit()
        return redirect(url_for('views.addsemester'))
        
    return render_template('add_department.html',semesters='semesters',user=current_user)    


@views.route('/addbook',methods=['GET','POST'])
def addbook():
    departments = Department.query.all()
    semesters = Semester.query.all()
    form = Addbooks(request.form)
    return render_template('addbook.html',title="Add book Page",form = form,user=current_user, departments=departments, semesters=semesters)
