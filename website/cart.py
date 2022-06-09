from flask import render_template, request, redirect, session
from flask_login import login_required, current_user, logout_user
from .views import *

cart = Blueprint('cart', __name__)

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False        

@cart.route('/addtocart', methods = ['POST'])
@login_required
@requires_access_level("student")
def AddCart():
    try:

        book_id = request.form.get('book_id')
        book = Addbook.query.filter_by(id = book_id).first()
        if book_id and request.method == "POST":
            DictItems = {book_id:{'name':book.name,'image':book.image_1, 'isbn':book.isbn, 'department':book.department.name, 'semester': book.semester.name}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if book_id in session['Shoppingcart']:
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)    
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)    

    except Exception as e :
        print(e)
    finally:
        return redirect(request.referrer)    

@cart.route('/cart')     
@login_required
@requires_access_level("student")
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) == 0:
        return redirect(url_for('views.student_home'))
    return render_template('cart.html', user = current_user)       


@cart.route('/deleteitem/<int:id>')
@login_required
@requires_access_level("student")
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0 :
        return redirect(url_for('views.student_home')) 
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('cart.getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart.getCart'))            


@cart.route('/emptycart')
@login_required
@requires_access_level("student")
def emptycart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('views.student_home'))
    except Exception as e:
        print(e)
        
            