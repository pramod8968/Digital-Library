from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_user import roles_required
from website.forms import Addbooks


views = Blueprint('views', __name__)

@views.route('/')
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

@views.route('/addbook',methods=['GET','POST'])
def addbook():
    form = Addbooks(request.form)
    return render_template('addbook.html',title="Add book Page",form = form,user=current_user)
