from .views import *


sem = Blueprint('sem', __name__)

@sem.route('/semesters')
@login_required
@requires_access_level("admin")
def semesters():
    se = Semester.query.order_by(Semester.id.desc()).all()
    return render_template('departments.html', title="Semesters Page",semesters=se,user=current_user)