from .views import *


show = Blueprint('show', __name__)

@show.route('/semesters')
@login_required
@requires_access_level("admin")
def semesters():
    se = Semester.query.order_by(Semester.id.desc()).all()
    return render_template('departments.html', title="Semesters Page",semesters=se,user=current_user)

@show.route('/departments')
@login_required
@requires_access_level("admin")
def departments():
    dept = Department.query.order_by(Department.id.desc()).all()
    return render_template('departments.html', title="Departments Page",departments=dept,user=current_user)

@show.route('/student_list')
@login_required
@requires_access_level("admin")
def student_list():
    stu = User.query.all()
    return render_template('users_list.html',students=stu,user=current_user)

