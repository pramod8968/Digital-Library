from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, logout_user
from requests import session
from .views import *

cart = Blueprint('cart', __name__)

@cart.route('/addtocart', methods = ['POST'])
@login_required
@requires_access_level("student")
def AddCart():
    try:
        book_id = request.form.get('book_id')
        book = Addbook.query.filter_by(id = book_id).first()
        if book_id and request.method == "POST":
            DictItems = {book_id:{'name':book.name, 'price':book.price, 'image':book.image_1}}

            if 'Shopcart' in session:
                print(session['Shoppingcart'])
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)    

    except Exception as e :
        print(e)
    finally:
        return redirect(request.referrer)    

