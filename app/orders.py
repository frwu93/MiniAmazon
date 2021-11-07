from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.product import Product
from flask import render_template, redirect, url_for, flash, request



from flask import Blueprint
bp = Blueprint('orders', __name__)


@bp.route('/checkout', methods=['GET'])
def checkout():
    print("checking out")
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id) #TODO: make this goddamn fcn
        address = User.
        subtotal = Cart.get_subtotal(cart_items)
    else:
        cart_items = None
    return render_template('checkout.html', title='Checkout', cart_items=cart_items, subtotal = subtotal)


@bp.route('/checkout/success', methods=['GET'])
def checkout_success():
    ##Must verify that a) enough supply b) enough monie
    return render_template('order_success.html', title='Order Success')

