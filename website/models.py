from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 


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

             