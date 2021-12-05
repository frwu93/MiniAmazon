from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.user import User
from .models.product import Product
from .models.order import Order

from .carts import calculate_payment

from flask import render_template, redirect, url_for, flash, request



from flask import Blueprint
bp = Blueprint('orders', __name__)


@bp.route('/checkout', methods=['GET'])
def checkout():
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id) 
        if len(cart_items) == 0:
            flash(f'Your cart is empty! Please add items before checking out.')
            return redirect(url_for('carts.cart'))
        user = User.get(current_user.id)
        payment = calculate_payment(cart_items)
    else:
        cart_items = None
    return render_template('checkout.html', title='Checkout', cart_items=cart_items, payment = payment, user = user)


@bp.route('/checkout/verify')
def verify_transaction():
    print('verifying transaction')
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id)
        if len(cart_items) == 0:
            return redirect(url_for('orders.checkout'))
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
    cart_items = Cart.get_cart_products_by_uid(current_user.id)
    payment = calculate_payment(cart_items)
    order_id = Order.add_order(current_user.id, payment["total"])
    Order.add_to_history(order_id, cart_items)
    User.updateBalanceWithdrawal(current_user.id, payment["total"])
    for item in cart_items:
        User.updateBalanceDeposit(item.seller_id, item.price * item.quantity)
    Product.decrease_purchased_quantity(cart_items)
    Cart.clear_user_cart(current_user.id)
    return render_template('order_success.html', title='Order Success', user = User.get(current_user.id), order_id = order_id, cart_items = cart_items, payment = payment)

