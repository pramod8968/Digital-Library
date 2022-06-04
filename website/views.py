from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, logout_user
from flask import flash
from flask import url_for
from numpy import product
from . import db,photos
from website.forms import Addbooks
from .models import Department,Semester,Addbook 
import secrets
from functools import wraps

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Login to Access', 'error')
                return redirect(url_for('views.home'))
            if current_user.get_urole()!=access_level:
                logout_user()
                flash('You do not have access to this resource. You have been automatically Logged Out', 'error')
                return redirect(url_for('views.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home_page.html", user=current_user)

@views.route('/student_home')
@login_required
@requires_access_level("student")
def student_home():
    # books = Addbook.query.filter(Addbook.stock > 0)
    page = request.args.get('page',1, type=int)
    departments = Department.query.join(Addbook, (Department.id == Addbook.department_id)).all()
    semesters = Semester.query.join(Addbook, (Semester.id == Addbook.semester_id)).all()
    books = Addbook.query.filter(Addbook.stock>=0).order_by(Addbook.id.desc()).paginate(page = page, per_page = 8)
    return render_template("student_home.html", user=current_user, books = books, departments = departments, semesters = semesters)


@views.route('/book/<int:id>')
@login_required
@requires_access_level("student")
def single_page(id):
    book = Addbook.query.get_or_404(id)
    departments = Department.query.join(Addbook, (Department.id == Addbook.department_id)).all()
    semesters = Semester.query.join(Addbook, (Semester.id == Addbook.semester_id)).all()
    return render_template('single_page.html', user = current_user, book = book, departments = departments, semesters = semesters )    

@views.route('/department/<int:id>')
@login_required
@requires_access_level("student")
def get_department(id):
    page = request.args.get('page',1, type=int)
    get_dep = Department.query.filter_by(id=id).first_or_404()
    department = Addbook.query.filter_by(department = get_dep).paginate(page = page, per_page = 8)
    departments = Department.query.join(Addbook, (Department.id == Addbook.department_id)).all()
    semesters = Semester.query.join(Addbook, (Semester.id == Addbook.semester_id)).all()
    return render_template('student_home.html', department = department, user = current_user, departments = departments, semesters = semesters, get_dep = get_dep)

@views.route('/semester/<int:id>')
@login_required
@requires_access_level("student")
def get_semester(id):
    page = request.args.get('page',1, type=int)
    get_sem = Semester.query.filter_by(id=id).first_or_404()
    semester = Addbook.query.filter_by(semester = get_sem).paginate(page = page, per_page = 8)
    semesters = Semester.query.join(Addbook, (Semester.id == Addbook.semester_id)).all()
    departments = Department.query.join(Addbook, (Department.id == Addbook.department_id)).all()
    return render_template('student_home.html', semester = semester, user = current_user, semesters = semesters, departments = departments, get_sem = get_sem)    


@views.route('/admin_home')
@login_required
@requires_access_level("admin")
def admin_home():
    books = Addbook.query.all()
    return render_template("admin_home.html", user=current_user,books=books)

@views.route('/teacher_home')
@login_required
@requires_access_level("teacher")
def teacher_home():
    return render_template("teacher_home.html", user=current_user)

@views.route('/aboutUs')
def about_us():
    return render_template("About_Us.html", user=current_user)
