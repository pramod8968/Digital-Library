from turtle import title
from website import create_app


import mysql.connector
import os  

app = create_app()
app.secret_key=os.urandom(24)


if __name__=='__main__':
    app.run(debug="True")