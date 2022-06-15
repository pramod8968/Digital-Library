from flask import render_template, request, redirect, session
from flask_login import login_required, current_user, logout_user

from website.models import Student_Cart
from .track import notify_click_track
from .views import *
from datetime import datetime

cart = Blueprint('cart', __name__)

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False        

@cart.route('/addtocart', methods = ['POST'])
@login_required
@requires_access_level(["student","admin"])
def AddCart():
    if current_user.is_authenticated:
        student_id = current_user.id
    try:
        book_id = request.form.get('book_id')
        book = Addbook.query.filter_by(id = book_id).first()
        if book_id and request.method == "POST":
            DictItems = {book_id:{'name':book.name,'image':book.image_1, 'isbn':book.isbn, 'department':book.department.name, 'semester': book.semester.name,'available_copies':book.available_copies}}
            if 'Shoppingcart' in session:
                pass
                # print(session['Shoppingcart'])
                if book_id in session['Shoppingcart']:
                    pass
                    # print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    cart = Student_Cart.query.filter_by(student_id = student_id).first()
                    if cart:
                        cart.carts = session['Shoppingcart']
                        db.session.commit()
                    else:
                        cart = Student_Cart(student_id = student_id, carts = session['Shoppingcart'])    
                        db.session.add(cart)
                        db.session.commit()
                    return redirect(request.referrer)    
            else:
                session['Shoppingcart'] = DictItems
                cart = Student_Cart.query.filter_by(student_id = student_id).first()
                if cart:
                    cart.carts = session['Shoppingcart']
                    db.session.commit()
                else:
                    cart = Student_Cart(student_id = student_id, carts = session['Shoppingcart'])    
                    db.session.add(cart)
                    db.session.commit()

                return redirect(request.referrer)    

            
    except Exception as e :
        print(e)
    finally:
        return redirect(request.referrer)    

@cart.route('/cart')     
@login_required
@requires_access_level(["student","admin"])
def getCart():
    if current_user.is_authenticated:
        student_id = current_user.id
    cart = Student_Cart.query.filter_by(student_id = student_id).first()
    if(cart):
        return render_template('cart.html', user = current_user,cart_items=cart.carts)
    return redirect(url_for('views.student_home'))       


@cart.route('/deleteitem/<int:id>')
@login_required
@requires_access_level(["student","admin"])
def deleteitem(id):
    if current_user.is_authenticated:
        student_id = current_user.id
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0 :
        return redirect(url_for('views.student_home')) 
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)

                cart = Student_Cart.query.filter_by(student_id = student_id).first()
                if cart:
                    cart.carts = session['Shoppingcart']
                    db.session.commit()
                else:
                    cart = Student_Cart(student_id = student_id, carts = session['Shoppingcart'])    
                    db.session.add(cart)
                    db.session.commit()
                return redirect(url_for('cart.getCart'))

    except Exception as e:
        print(e)
        return redirect(url_for('cart.getCart'))            


@cart.route('/emptycart')
@login_required
@requires_access_level(["student","admin"])
def emptycart():
    if current_user.is_authenticated:
        student_id = current_user.id
    try:
        session.pop('Shoppingcart', None)
        cart = Student_Cart.query.filter_by(student_id = student_id).first()
        if cart:
            db.session.delete(cart)
            db.session.commit()
        return redirect(url_for('views.student_home'))
    except Exception as e:
        print(e)


@cart.route('/order/<int:book_id>', methods=["GET","POST"])
@login_required
@requires_access_level(["student","admin"])
def order(book_id):
    if current_user.is_authenticated:
        if(current_user.urole=="admin"):
            book = Addbook.query.get_or_404(book_id)
            if(book.available_copies==0):
                flash("No Copies Available", 'danger')  
                return redirect(url_for('views.admin_home'))
            usn = request.form.get("usn")
            student = User.query.filter_by(usn=usn).first()
            if(student):
                student_id=student.id
            else:
                flash("No student with Given USN", 'danger')  
                return redirect(url_for('views.admin_home'))
        else:
            student_id = current_user.id
        role = current_user.urole
    orders = Student_Order.query.filter_by(student_id=student_id).all() 
    if orders:
        for order in orders:
            if(order.book_id==book_id and order.status in ["Requested","Issued"]):
                flash(f"You have already ordered this book", 'danger')  
                if(role in ["student","teacher"]):
                    return redirect(url_for('cart.getCart')) 
                else:
                    return redirect(url_for('views.admin_home'))
        order = Student_Order(student_id=student_id,book_id=book_id,request_time=datetime.now())
        db.session.add(order)
        db.session.commit()
        if(role in ["student","teacher"]):
            flash(f"Your order request has been sent for Library Admin", 'success') 
            return redirect(url_for('views.show_student_order'))
        else:
            flash(f"Book Order placed successfully", 'success') 
            return redirect(url_for('views.admin_home'))
    else:
        order = Student_Order(student_id=student_id,book_id=book_id,request_time=datetime.now())
        db.session.add(order)
        db.session.commit()
        flash(f"Your order request has been sent for Library Admin", 'success') 
        return redirect(url_for('views.show_student_order'))
    


@cart.route('/cancel_order/<int:order_id>')
@login_required
@requires_access_level(["student","admin"])
def cancel_order(order_id):
    order = Student_Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order cancelled successfully !!!','success')
    return redirect(url_for('views.show_student_order'))


@cart.route('/notify_me/<id>')
@login_required
@requires_access_level(["student","admin"])
def notify(id):
    notify_click_track(id)
    return redirect(url_for('views.student_home'))

    

     



            