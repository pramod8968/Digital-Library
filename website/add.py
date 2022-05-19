from .views import *
import pandas as pd

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
        desc = form.discription.data
        department = request.form.get('department')
        semester = request.form.get('semester') 
        image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")       
        #image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
        #image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")
        addpro = Addbook(name=name, price=price, isbn=isbn,stock=stock,desc=desc,department_id=department,semester_id=semester,image_1=image_1,image_2="No IMG",image_3="No IMG")
        flash(f'The book {name} has been added to your database','success')
        db.session.add(addpro)
        db.session.commit()
        return redirect(url_for('views.admin_home'))
    return render_template('addbook.html',title="Add book Page",form = form,user=current_user, departments=departments, semesters=semesters)



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
                stock = df.loc[df["isbn"]==isbn, 'stock'].values[0]
                desc = df.loc[df["isbn"]==isbn, 'desc'].values[0]
                department = df.loc[df["isbn"]==isbn, 'department_id'].values[0]
                semester = df.loc[df["isbn"]==isbn, 'semester_id'].values[0]
                image_1 = "No IMG"
                addpro = Addbook(name=name, price=price, isbn=isbn,stock=stock,desc=desc,department_id=department,semester_id=semester,image_1=image_1,image_2="No IMG",image_3="No IMG")
                db.session.add(addpro)
                db.session.commit()
        flash('Books Data Added Successfully', category='success')  
    return render_template('addbulkbooks.html',user=current_user)
