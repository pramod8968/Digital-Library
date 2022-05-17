from turtle import title
from website import create_app
from flask import render_template, request,flash 
from website.forms import Addbooks

import mysql.connector
import os  

app = create_app()
app.secret_key=os.urandom(24)

@app.route('/addbook',methods=['GET','POST'])
def addbook():
    form = Addbooks(request.form)
    return render_template('addbook.html',title="Add book Page",form = form)


if __name__=='__main__':
    app.run(debug="True")