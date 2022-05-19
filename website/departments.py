
from .views import *


dep = Blueprint('dep', __name__)

@dep.route('/departments')
@login_required
@requires_access_level("admin")
def departments():
    dept = Department.query.order_by(Department.id.desc()).all()
    return render_template('departments.html', title="Departments Page",departments=dept)

