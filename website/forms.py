
from flask_wtf.file import FileAllowed,FileField,FileRequired
from wtforms import Form, IntegerField, StringField,BooleanField,TextAreaField, validators


class Addbooks(Form):
    name = StringField('Name',[validators.DataRequired()])
    price = IntegerField('Price',[validators.DataRequired()])
    isbn = IntegerField('isbn', default=0)
    stock = IntegerField('Stock',[validators.DataRequired()])
    discription = TextAreaField('Discription',[validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'],'images only please')])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg','png','gif','jpeg'],'images only please')])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg','png','gif','jpeg'],'images only please')])


