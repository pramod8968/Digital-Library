from .views import *

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
        image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")
        addpro = Addbook(name=name, price=price, isbn=isbn,stock=stock,desc=desc,department_id=department,semester_id=semester,image_1=image_1,image_2="No IMG",image_3="No IMG")
        flash(f'The book {name} has been added to your database','success')
        db.session.add(addpro)
        db.session.commit()
        return redirect(url_for('views.admin_home'))
    return render_template('addbook.html',title="Add book Page",form = form,user=current_user, departments=departments, semesters=semesters)
