from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 


from datetime import datetime


class Addbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    isbn = db.Column(db.Integer,default=0)
    stock = db.Column(db.Integer,nullable=False)
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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name






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

        def __init__(self,first_name,password,email,is_active,urole,usn):
                self.username = first_name
                self.password = password
                self.email = email
                self.is_active = is_active
                self.urole = urole
                self.usn = usn

        def get_id(self):
                return self.id
        def is_active(self):
                return self.is_active
        def activate_user(self):
                self.is_active = True         
        def get_username(self):
                return self.username
        def get_urole(self):
                return self.urole
        def get_usn(self):
                return self.usn

             