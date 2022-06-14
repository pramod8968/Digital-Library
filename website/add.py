from turtle import title
from .views import *
import pandas as pd
import os
from flask import current_app
from werkzeug.security import check_password_hash

add = Blueprint('add', __name__)

@add.route('/adddepartment', methods=['GET','POST'])
@login_required
@requires_access_level("admin")
def adddepartment():
    if request.method == "POST":
        getdepartment = request.form.get('department')
        department = Department(name=getdepartment)
        db.session.add(department)
        flash(f'The Department {getdepartment} was added to your database','success')
        db.session.commit()
        return redirect(url_for('add.adddepartment'))
    return render_template('add_department.html', departments='departments', user=current_user)

@add.route('/updatedepartment/<int:id>', methods=['GET','POST'])
@login_required
@requires_access_level("admin")
def updatedepartment(id):
    updatedepartment = Department.query.get_or_404(id)
    department = request.form.get('department')
    if request.method == 'POST':
        updatedepartment.name = department 
        flash(f'Department has been updated successfully.', 'success')
        db.session.commit()
        return redirect(url_for('dep.departments'))
    return render_template('updatedepartment.html', title = 'Update Department', user = current_user, updatedepartment = updatedepartment)


@add.route('/deletedepartment/<int:id>', methods=['GET','POST'])
@login_required
@requires_access_level("admin")
def deletedepartment(id):
    department = Department.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(department)
        db.session.commit()
        flash(f'Department {department.name} was deleted successfully from your database', 'success')
        return redirect(url_for('views.admin_home'))
    flash(f'Department {department.name} can\'t be deleted', 'warning')
    return redirect(url_for('views.admin_home'))    


@add.route('/addsemester', methods=['GET','POST'])
@login_required
@requires_access_level("admin")
def addsemester():
    if request.method == "POST":
        getsemester = request.form.get('semester')
        semester = Semester(name=getsemester)
        db.session.add(semester)
        flash(f'The Semester {getsemester} was added to your database','success')
        db.session.commit()
        return redirect(url_for('add.addsemester'))
        
    return render_template('add_department.html',semesters='semesters',user=current_user)  


@add.route('/updatesemester/<int:id>', methods=['GET','POST'])
@login_required
@requires_access_level("admin")
def updatesemester(id):
    updatesemester = Semester.query.get_or_404(id)
    semester = request.form.get('semester')
    if request.method == 'POST':
        updatesemester.name = semester 
        flash(f'Semester has been updated successfully.', 'success')
        db.session.commit()
        return redirect(url_for('sem.semesters'))
    return render_template('updatedepartment.html', title = 'Update Semester', user = current_user, updatesemester = updatesemester)      


@add.route('/deletesemester/<int:id>', methods=['GET','POST'])
@login_required
@requires_access_level("admin")
def deletesemester(id):
    semester = Semester.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(semester)
        db.session.commit()
        flash(f'Semester {semester.name} was deleted successfully from your database', 'success')
        return redirect(url_for('views.admin_home'))
    flash(f'Semester {semester.name} can\'t be deleted', 'warning')
    return redirect(url_for('views.admin_home'))    


@add.route('/addbook',methods=['GET','POST'])
@requires_access_level("admin")
def addbook():
    departments = Department.query.all()
    semesters = Semester.query.all()
    form = Addbooks(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        isbn = form.isbn.data 
        stock = form.stock.data 
        available_copies = stock
        desc = form.discription.data
        department = request.form.get('department')
        semester = request.form.get('semester') 
        image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")       
        #image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
        #image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")
        addpro = Addbook(name=name, price=price, isbn=isbn,stock=stock,desc=desc,department_id=department,semester_id=semester,image_1=image_1,image_2="No IMG",image_3="No IMG", available_copies = available_copies)
        flash(f'The book {name} has been added to your database','success')
        db.session.add(addpro)
        db.session.commit()
        return redirect(url_for('views.admin_home'))
    return render_template('addbook.html',title="Add book Page",form = form,user=current_user, departments=departments, semesters=semesters)


@add.route('/updatebook/<int:id>',methods=['GET','POST'])
@requires_access_level("admin")
def updatebook(id):
    departments = Department.query.all()
    semesters = Semester.query.all()
    book = Addbook.query.get_or_404(id)
    department = request.form.get('department')
    semester = request.form.get('semester')
    form = Addbooks(request.form)
    if request.method == "POST":
        book.name = form.name.data
        book.price = form.price.data 
        book.isbn = form.isbn.data
        ac = form.stock.data - book.stock 
        book.stock = form.stock.data 
        book.available_copies = book.available_copies + ac
        book.desc = form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + book.image_1))
                book.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            except:
                book.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'Book has been updated successfully', 'success')
        return redirect(url_for('views.admin_home'))
    form.name.data = book.name 
    form.price.data = book.price
    form.isbn.data = book.isbn
    form.stock.data = book.stock
    form.discription.data = book.desc
    return render_template('updatebook.html', form = form, user=current_user, departments = departments, semesters = semesters, book = book )

@add.route('/deletebook/<int:id>', methods=['POST'])
@requires_access_level("admin")
def deletebook(id):
    book = Addbook.query.get_or_404(id) 
    if request.method == "POST":
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + book.image_1))
            except Exception as e:
                print(e)
        db.session.delete(book)  
        db.session.commit()
        flash(f'The book {book.name} was deleted successfully from your database.', 'success') 
        return redirect(url_for('views.admin_home')) 

    flash(f"Can't delete the book", 'danger')            
    return redirect(url_for('views.admin_home'))


@add.route('/addbulk',methods=['GET','POST'])
@requires_access_level("admin")
def addbookbulk():
    f = request.files.getlist("file")
    for file in f:
        fname=file.filename
        fname = fname.split(".",1)
        fname = fname[0]

        if file:
            df = pd.DataFrame(pd.read_excel(file))
            print(df)
            for isbn in df.isbn:
                name = df.loc[df["isbn"]==isbn, 'Book_Name'].values[0]
                price = df.loc[df["isbn"]==isbn, 'Price'].values[0]
                stock = int(df.loc[df["isbn"]==isbn, 'stock'].values[0])
                desc = df.loc[df["isbn"]==isbn, 'desc'].values[0]
                department = int(df.loc[df["isbn"]==isbn, 'department_id'].values[0])
                semester = int(df.loc[df["isbn"]==isbn, 'semester_id'].values[0])
                image_1 = "No IMG"
                addpro = Addbook(name=name, price=price, isbn=isbn,stock=stock,desc=desc,department_id=department,semester_id=semester,image_1=image_1,image_2="No IMG",image_3="No IMG")
                db.session.add(addpro)
                db.session.commit()
        flash('Books Data Added Successfully', category='success')  
    return render_template('addbulkbooks.html',user=current_user)


@add.route('/update_profile',methods=['GET','POST'])
@requires_access_level("student")
def update_profile():
    id = current_user.id
    users = User.query.get_or_404(id)
    if request.method == "POST":
        if check_password_hash(users.password,request.form.get('password')):
            users.first_name = request.form.get('sname')
            users.email = request.form.get('semail') 
            db.session.commit()
            flash(f'Profile has been updated successfully', 'success')
            return redirect(url_for('add.update_profile'))  
        else:
            flash('Please Enter Correct Password to update the profile!!', category='error')
            return redirect(url_for('add.update_profile')) 
    return render_template('edit_profile.html', user=current_user, users = users )  

@add.route('/user_update/<id>')
def user_status(id):
    user = User.query.get_or_404(id)
    if(user.status=="Good"):
        user.status="Blocked"
    else:
        user.status="Good"
    db.session.commit()
    return redirect(url_for('show.student_list'))



