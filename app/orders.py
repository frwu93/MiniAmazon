from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.user import User
from .models.product import Product
from .models.order import Order

from flask import render_template, redirect, url_for, flash, request



from flask import Blueprint
bp = Blueprint('orders', __name__)


@bp.route('/checkout', methods=['GET'])
def checkout():
    print("checking out")
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id) 
        user = User.get(current_user.id)
        subtotal = Cart.get_subtotal(cart_items)
    else:
        cart_items = None
    return render_template('checkout.html', title='Checkout', cart_items=cart_items, subtotal = subtotal, user = user)


@bp.route('/checkout/verify')
def verify_transaction():
    print('verifying transaction')
    if current_user.is_authenticated:
        print('penis')
        cart_items = Cart.get_cart_products_by_uid(current_user.id)
        for item in cart_items:
            if item.quantity > Product.get(item.product_id).quantity:
                flash(f'There is not enough of {item.product_name} in stock! Please check the amount in stock.')
                return redirect(url_for('orders.checkout'))
        if float(User.get(current_user.id).balance) < float(Cart.get_subtotal(cart_items)):
            flash(f'Take some stuff out! You don\'t have enough in your balance!')
            return redirect(url_for('orders.checkout'))
        #successful transaction
        return redirect(url_for('orders.checkout_success'))
    else:
        redirect(url_for('index.index'))


@bp.route('/checkout/success', methods=['GET'])
def checkout_success():
    ##Must verify that a) enough supply b) enough monie
    order_id = Order.add_order(current_user.id)
    print(order_id)
    cart_items = Cart.get_cart_products_by_uid(current_user.id)
    print(cart_items)
    Order.add_to_history(order_id, cart_items)
    return render_template('order_success.html', title='Order Success')

