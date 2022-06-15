from flask import Blueprint, render_template, request, redirect, flash, url_for,session
from flask_login import login_required, current_user, logout_user
from flask import flash
from flask import url_for
from numpy import product
from . import db,photos,search
from website.forms import Addbooks
from .models import Department,Semester,Addbook, User , Student_Order, Student_Cart,Stats
import secrets
from functools import wraps
from .track import uvt,issue_track
import datetime
from .demand import demand_graph

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Login to Access', 'error')
                return redirect(url_for('views.home'))
            print(access_level)
            if current_user.get_urole() not in access_level:
                logout_user()
                flash('You do not have access to this resource. You have been automatically Logged Out', 'error')
                return redirect(url_for('views.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

views = Blueprint('views', __name__)

def departments():
    departments = Department.query.join(Addbook, (Department.id == Addbook.department_id)).all()
    return departments

def semesters():
    semesters = Semester.query.join(Addbook, (Semester.id == Addbook.semester_id)).all()
    return semesters


@views.route('/')
@views.route('/home')
def home():
    return render_template("home_page.html", user=current_user)

@views.route('/student_home')
@login_required
@requires_access_level("student")
def student_home():
    if current_user.is_authenticated:
        student_id = current_user.id
    cart = Student_Cart.query.filter_by(student_id = student_id).first()
    if(cart):
        session['Shoppingcart'] = cart.carts
    else:
        try:
            session.pop('Shoppingcart', None)
        except Exception as e:
            print(e)
    page = request.args.get('page',1, type=int)
    books = Addbook.query.filter(Addbook.stock>=0).order_by(Addbook.id.desc()).paginate(page = page, per_page = 8)
    return render_template("student_home.html", user=current_user, books = books, departments = departments(), semesters = semesters())


@views.route('/result')
@login_required
@requires_access_level("student")
def result():
    searchword =request.args.get('q')
    books = Addbook.query.msearch(searchword, fields=['name','desc', 'isbn'])
    # if searchword not in books:
    #     return render_template('booknotfound.html',user=current_user) 
    return render_template('result.html', user=current_user, books=books, departments = departments(), semesters = semesters(),searchword = searchword)


@views.route('/admin_result')
def admin_result():
    orders = Department.query.all()
    search_department =request.args.get('d')
    depts = Department.query.msearch(search_department, fields=['name'])
    # print(search_department)
    # search_semester =request.args.get('sem')
    # sems = Semester.query.msearch(search_semester, fields=['name'])
    # print(search_semester)
    # search_book =request.args.get('b')
    # books = Addbook.query.msearch(search_book, fields=['name'])
    # print(search_book)
    # search_usn =request.args.get('u')
    # usn = User.query.msearch(search_usn, fields=['usn'])
    # print(search_usn)
    # sems= sems,books = books,usn=usn,
    #  search_semester = search_semester,search_book = search_book, search_usn = search_usn
    return render_template('admin_result.html',user = current_user, depts=depts, departments = departments(), semesters = semesters(),search_department = search_department)


@views.route('/book/<int:id>')
@login_required
@requires_access_level(["student","admin"])
def single_page(id):
    uvt(id)
    book = Addbook.query.get_or_404(id)
    return render_template('single_page.html', user = current_user, book = book, departments = departments(), semesters = semesters() )    

@views.route('/department/<int:id>')
@login_required
@requires_access_level(["student","admin"])
def get_department(id):
    page = request.args.get('page',1, type=int)
    get_dep = Department.query.filter_by(id=id).first_or_404()
    department = Addbook.query.filter_by(department = get_dep).paginate(page = page, per_page = 8)
    return render_template('student_home.html', department = department, user = current_user, departments = departments(), semesters = semesters(), get_dep = get_dep)

@views.route('/semester/<int:id>')
@login_required
@requires_access_level(["student","admin"])
def get_semester(id):
    page = request.args.get('page',1, type=int)
    get_sem = Semester.query.filter_by(id=id).first_or_404()
    semester = Addbook.query.filter_by(semester = get_sem).paginate(page = page, per_page = 8)
    return render_template('student_home.html', semester = semester, user = current_user, semesters = semesters(), departments = departments(), get_sem = get_sem)    


@views.route('/orders')
@login_required
@requires_access_level(["student","admin"])  
def show_student_order():
    student_id = current_user.id
    orders = Student_Order.query.filter_by(student_id=student_id).all()
    return render_template('book_orders.html',user=current_user,orders=orders)

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

@views.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", user=current_user)


@views.route('/orders_list')
@requires_access_level("admin")
def orders_list_for_admin():
    orders = Student_Order.query.all()
    return render_template("orders_list_for_admin.html", user=current_user,orders=orders)    

@views.route('/orders_list/<status>', methods=['POST','GET'])
@requires_access_level("admin")
def orders_list_on_status(status):
    orders = Student_Order.query.filter_by(status=status)
    if request.method == "POST":
        status = request.form.get('status')
        status = status.split(',')
        id = int(status[1])
        order = Student_Order.query.get_or_404(id)
        order.status = status[0]
        if(order.status=="Issued"):
            book_id=order.book.id
            book = Addbook.query.get_or_404(book_id)
            book.available_copies = book.available_copies-1
            order.approve_time=datetime.datetime.now()
            return_date = datetime.datetime.now() + datetime.timedelta(days=7)
            order.return_time=return_date
            issue_track(order.book.id)
        elif(order.status=="Returned"):
            book_id=order.book.id
            book = Addbook.query.get_or_404(book_id)
            book.available_copies = book.available_copies+1
            order.returned_time = datetime.datetime.now()
        db.session.commit()
    return render_template("orders_list_for_admin.html", user=current_user,orders=orders,status=status)    


@views.route('/demand_graph/<book_id>', methods=['POST','GET'])
def show_demand_graph(book_id):
    book = Addbook.query.get_or_404(book_id)
    book_stats = Stats.query.filter_by(book_id=book_id).all()
    demand_graph(book,book_stats)
