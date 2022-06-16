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
import os

basedir=os.path.abspath(os.path.dirname(__file__))

from matplotlib.figure import Figure

import pandas as pd
from .models import Stats
from sqlalchemy import create_engine
import sqlalchemy
import sqlite3
import numpy as np
import pickle
import sklearn

import matplotlib
matplotlib.use('Qt5agg')
import matplotlib.pyplot as plt


import pandas as pd
import os
from flask import current_app
from io import BytesIO
import base64


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Login to Access', 'error')
                return redirect(url_for('views.home'))
            # print(access_level)
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

@views.route('/admin_home_result_for_book')
@login_required
@requires_access_level("admin")
def admin_home_book_search():
    search_book = request.args.get('a')
    result_book = Addbook.query.msearch(search_book, fields = ['name'])
    return render_template('admin_home_result.html', user = current_user,departments = departments(), semesters = semesters(), search_book = search_book, result_book = result_book )

@views.route('/admin_home_result_for_isbn')
@login_required
@requires_access_level("admin")
def admin_home_isbn_search():
    search_isbn = request.args.get('i')
    result_isbn = Addbook.query.msearch(search_isbn, fields = ['isbn'])
    return render_template('admin_home_result.html', user = current_user,departments = departments(), semesters = semesters(), search_isbn = search_isbn, result_isbn = result_isbn )


@views.route('/admin_orders_book_result/<status>/')
def admin_orders_book_search(status):
    search_ordered_book =request.args.get('b')
    result_ordered_book = Addbook.query.msearch(search_ordered_book, fields=['name'])
    li = []
    for book in result_ordered_book:
        li.append(book.id) 
    orders = Student_Order.query.filter(Student_Order.book_id.in_(li),Student_Order.status==status)
    return render_template('admin_result.html',user = current_user, result_ordered_book=orders, status = status, departments = departments(), semesters = semesters(),search_ordered_book = search_ordered_book)


@views.route('/admin_orders_usn_result/<status>/')
def admin_orders_usn_search(status):
    search_usn =request.args.get('u')
    result_usn = User.query.msearch(search_usn, fields=['usn'])
    li = []
    for usn in result_usn:
        li.append(usn.id) 
    orders = Student_Order.query.filter(Student_Order.student_id.in_(li),Student_Order.status==status)
    return render_template('admin_result.html',user = current_user, result_usn=orders, status = status, departments = departments(), semesters = semesters(),search_usn = search_usn)


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
    orders = Student_Order.query.filter_by(student_id=student_id).order_by(Student_Order.request_time.desc())
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
    orders = Student_Order.query.order_by(Student_Order.request_time.desc()).all()
    return render_template("orders_list_for_admin.html", user=current_user,orders=orders)    

@views.route('/orders_list/<status>', methods=['POST','GET'])
@requires_access_level("admin")
def orders_list_on_status(status):
    orders = Student_Order.query.filter_by(status=status).order_by(Student_Order.request_time.desc())
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
            order.number_of_copies=book.stock
            return_date = datetime.datetime.now() + datetime.timedelta(days=7)
            order.return_time=return_date
            issue_track(order.book.id)
        elif(order.status=="Returned"):
            book_id=order.book.id
            book = Addbook.query.get_or_404(book_id)
            book.available_copies = book.available_copies+1
            order.number_of_copies=book.stock
            order.returned_time = datetime.datetime.now()
            delay = order.returned_time.date() - order.return_time.date()
            if(delay.days>0):
                fine = delay.days*10
            else:
                fine = 0
            order.fine = fine
        db.session.commit()
    return render_template("orders_list_for_admin.html", user=current_user,orders=orders,status=status)    

@views.route('/demand_graph/<book_ids>', methods=['POST','GET'])
def show_demand_graph(book_ids):

    file = open(basedir+"/model.pickle",'rb')
    model = pickle.load(file)
    book = Addbook.query.get_or_404(book_ids)

    img = BytesIO()
    stats = Stats.query.filter_by(book_id=book.id).all()
    df = pd.DataFrame(columns=['id','week_stamp','book_id','demand_time','dt','number_of_issues','number_notify_me','unique_visits','Demand','number_of_copies'])
    i = 0
    for stat in stats:
        stat.demand = int(model.predict([[stat.dt,stat.number_of_copies,stat.number_of_issues,stat.number_notify_me,stat.unique_visits]])[0])
        df.loc[i] = [stat.id, stat.week_stamp, stat.book_id,stat.demand_time,stat.dt,stat.number_of_issues,stat.number_notify_me,stat.unique_visits,stat.demand,stat.number_of_copies] 
        i=i+1
    plot_df = df[['week_stamp','number_of_copies','Demand']]

    data_sums = df.sum(axis = 0, skipna = True)
    demand_mean = [np.mean(df.Demand)]*len(plot_df)
    demand_mean_value = plot_df['Demand'].rolling(window=12).mean()

    nc_mean_value = plot_df['number_of_copies'].rolling(window=12).mean()

    plt.plot(plot_df.Demand, label = "Demand")
    plt.plot(plot_df.number_of_copies, label = "Number of Copies")
    plt.plot(demand_mean_value, label = "Demand Mean Curve")
    plt.plot(nc_mean_value, label = "Available Copies Mean Curve")

    # fig = Figure()
    # ax = fig.subplots()
    # ax.plot(plot_df.Demand, label = "Demand")
    # ax.plot(plot_df.number_of_copies, label = "Number of Copies")
    # ax.plot(demand_mean_value, label = "Demand Mean Curve")
    # ax.plot(nc_mean_value, label = "Available Copies Mean Curve")

    plt.legend()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    db.session.commit()

    return render_template("demand_graph.html",plot_url = plot_url,book=book,data_sums=data_sums)


