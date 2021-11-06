from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.product import Product


from flask import Blueprint
bp = Blueprint('carts', __name__)


#api endpoints: checkout, delete item, change quantity, 

@bp.route('/cart', methods=['GET'])
def cart():
    print("go to cart")
    if current_user.is_authenticated:
        cart_items = Cart.get_all_by_uid(current_user.id) #TODO: make this goddamn fcn
        sellers = []
        for item in cart_items:
            sellers.append(Product.)
    else:
        cart_items = None
    return render_template('cart.html', title='Cart', cart_items=cart_items)


    



