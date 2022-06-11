from email.policy import default
from pickle import TRUE
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 


from datetime import datetime


class Addbook(db.Model):
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
        book_id = db.Column(db.Integer, db.ForeignKey('addbook.id'), nullable = True)
        book = db.relationship('Addbook', backref=db.backref('books', lazy = True))

        date_stamp =db.Column(db.Date, nullable = False)

        demand_time = db.Column(db.String(20), default="Normal")
        
        dt = db.Column(db.Float, default = 0.1)
        number_of_issues = db.Column(db.Integer, default = 0)
        number_notify_me = db.Column(db.Integer, default = 0)
        unique_visits = db.Column(db.Integer, default= 0)
        demand = db.Column(db.Float, default = 0)




class Department(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(30), nullable = False, unique = True)

class Semester(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(30), nullable = False, unique = True)

class User(db.Model,UserMixin):

        __tablename__='user'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(150), unique=True)
        password=db.Column(db.String(150))
        first_name=db.Column(db.String(150))
        is_active = db.Column(db.Boolean,default=False)
        urole = db.Column(db.String(80))
        usn = db.Column(db.String(10))


        department_id = db.Column(db.Integer, db.ForeignKey('department.id'),nullable=True)
        department = db.relationship('Department', backref=db.backref('user_departments',lazy=True))

        semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'),nullable=True)
        semester = db.relationship('Semester', backref=db.backref('user_semesters',lazy=True)) 

        def __init__(self,first_name,password,email,is_active,urole,usn,department_id=0,semester_id=0):
                self.first_name = first_name
                self.password = password
                self.email = email
                self.is_active = is_active
                self.urole = urole
                self.usn = usn
                self.department_id = department_id
                self.semester_id=semester_id

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

             