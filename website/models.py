from email.policy import default
from enum import unique
from pickle import TRUE

from sqlalchemy import null
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 
import json


from datetime import datetime


class Addbook(db.Model):
    __tablename__='addbook'
    __searchable__ = ['name', 'desc', 'isbn']    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    isbn = db.Column(db.Integer,default=0)
    stock = db.Column(db.Integer,nullable=False)
    available_copies = db.Column(db.Integer,nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'),nullable=False)
    department = db.relationship('Department', backref=db.backref('departments',lazy=True))

    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'),nullable=False)
    semester = db.relationship('Semester', backref=db.backref('semesters',lazy=True)) 

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')  
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg') 
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')  

    def __repr__(self):
        return '<Post %r>' % self.name

class Stats(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        week_stamp =db.Column(db.String(10), nullable = False)
        book_id = db.Column(db.Integer, db.ForeignKey('addbook.id'), nullable = True)
        book = db.relationship('Addbook', backref=db.backref('books', lazy = True))

        demand_time = db.Column(db.String(20), default="Normal")
        
        dt = db.Column(db.Float, default = 0.1)
        number_of_issues = db.Column(db.Integer, default = 0)
        number_notify_me = db.Column(db.Integer, default = 0)
        unique_visits = db.Column(db.Integer, default= 0)
        number_of_copies = db.Column(db.Integer,default= 50)
        demand = db.Column(db.Float, default = 0)

        def __init__(self,book_id,week_stamp,demand_time="Normal",dt=0.1,number_of_issues=0,number_notify_me=0,unique_visits=0,demand=0,number_of_copies=0):
                self.book_id=book_id
                self.week_stamp=week_stamp
                self.demand_time=demand_time
                self.dt = dt
                self.number_of_issues=number_of_issues
                self.number_notify_me=number_notify_me
                self.unique_visits=unique_visits
                self.demand=demand
                self.number_of_copies = number_of_copies


class JsonEncodedDict(db.TypeDecorator):
        impl = db.Text

        def process_bind_param(self, value, dialect):
                if value is None:
                        return '{}'
                else:
                        return json.dumps(value)

        def process_result_value(self, value, dialect):
                if value is None:
                        return {}
                else:
                        return json.loads(value)                                

class Student_Order(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        status = db.Column(db.String(20), default = 'Requested', nullable = False)
        request_time = db.Column(db.DateTime, nullable = True)
        approve_time = db.Column(db.DateTime, nullable = True)
        return_time = db.Column(db.DateTime, nullable = True)
        returned_time = db.Column(db.DateTime, nullable = True)

        student_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
        student = db.relationship('User', backref=db.backref('students_order',lazy=True))

        book_id = db.Column(db.Integer, db.ForeignKey('addbook.id'),nullable=True)
        book = db.relationship('Addbook', backref=db.backref('books_order',lazy=True))
        fine = db.Column(db.Float,default=0)


class Student_Cart(db.Model):
        id = db.Column(db.Integer, primary_key = True)  

        student_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
        student = db.relationship('User', backref=db.backref('students_cart',lazy=True))

        carts = db.Column(JsonEncodedDict)

class Issues_data(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        time_stamp = db.Column(db.DateTime,nullable=True)
        book_id = db.Column(db.Integer, db.ForeignKey('addbook.id'), nullable = True)
        book = db.relationship('Addbook', backref=db.backref('books_issue', lazy = True))

        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
        user = db.relationship('User', backref=db.backref('issuer_name', lazy = True))

        status = db.Column(db.String(30), nullable=True)


class Department(db.Model):
        __searchable__ = ['name'] 
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(30), nullable = False, unique = True)

class Semester(db.Model):
        __searchable__ = ['name']
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(30), nullable = False, unique = True)

class User(db.Model,UserMixin):
        __searchable__ = ['usn']
        __tablename__='user'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(150), unique=True)
        password=db.Column(db.String(150))
        first_name=db.Column(db.String(150))
        is_active = db.Column(db.Boolean,default=False)
        urole = db.Column(db.String(80))
        usn = db.Column(db.String(10))
        status = db.Column(db.String(10))


        department_id = db.Column(db.Integer, db.ForeignKey('department.id'),nullable=True)
        department = db.relationship('Department', backref=db.backref('user_departments',lazy=True))

        semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'),nullable=True)
        semester = db.relationship('Semester', backref=db.backref('user_semesters',lazy=True)) 

        def __init__(self,first_name,password,email,is_active,urole,usn,department_id=0,semester_id=0, status = "Good"):
                self.first_name = first_name
                self.password = password
                self.email = email
                self.is_active = is_active
                self.urole = urole
                self.usn = usn
                self.department_id = department_id
                self.semester_id=semester_id
                self.status = status

        def get_id(self):
                return self.id
        def is_active(self):
                return self.is_active
        def activate_user(self):
                self.is_active = True         
        def get_username(self):
                return self.first_name
        def get_urole(self):
                return self.urole
        def get_usn(self):
                return self.usn
        def __repr__(self):
            return '<Post %r>' % self.name

             