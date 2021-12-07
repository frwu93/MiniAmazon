from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.user import User
from .models.product import Product
from .models.order import Order
from .models.coupon import Coupon

from .carts import calculate_payment

from flask import render_template, redirect, url_for, flash, request



from flask import Blueprint
bp = Blueprint('orders', __name__)


@bp.route('/checkout/', methods=['GET'])
@bp.route('/checkout/<coupon>', methods=['GET'])
def checkout(coupon = None):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    print("CHECKOUT")
    print(coupon)
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id) 
        if len(cart_items) == 0:
            flash(f'Your cart is empty! Please add items before checking out.')
            return redirect(url_for('carts.cart'))
        user = User.get(current_user.id)
        code = None
        if coupon is not None:
            coupon = Coupon.find_coupon(coupon)
            code = coupon.code
            print("COUPON IS ")
            print(coupon)
        payment = calculate_payment(cart_items, coupon)
    else:
        cart_items = None
    return render_template('checkout.html', title='Checkout', cart_items=cart_items, payment = payment, user = user, coupon = coupon)


@bp.route('/checkout/verify/')
@bp.route('/checkout/verify/<coupon>')
def verify_transaction(coupon = None):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    print('verifying transaction')
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id)
        code = None
        if coupon is not None:
            coupon = Coupon.find_coupon(coupon)
            code = coupon.code
            print(coupon.code)
        payment = calculate_payment(cart_items, coupon)
        if len(cart_items) == 0:
            return redirect(url_for('orders.checkout'))
        for item in cart_items:
            if item.quantity > Product.get(item.product_id).quantity:
                flash(f'There is not enough of {item.product_name} in stock! Please check the amount in stock.')
                return redirect(url_for('orders.checkout'))
        if float(User.get(current_user.id).balance) < float(payment['total']):
            flash(f'You don\'t have enough in your balance to complete this purchase!')
            return redirect(url_for('orders.checkout'))
        #successful transaction
        curBalance = float(User.get(current_user.id).balance)
        for item in cart_items:
            individualCost =calculate_payment([item], coupon)['total']
            curBalance -= individualCost
            User.add_purchase(current_user.id, individualCost, datetime.datetime.now(), curBalance, item.product_name, item.quantity)
        return redirect(url_for('orders.checkout_success', coupon = code))   
    else:
        redirect(url_for('index.index'))


@bp.route('/checkout/success', methods=['GET'])
@bp.route('/checkout/success/<coupon>', methods=['GET'])
def checkout_success(coupon = None):
    ##Must verify that a) enough supply b) enough monie
    cart_items = Cart.get_cart_products_by_uid(current_user.id)
    print("NOTICE ME")
    print(coupon)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    coupon = Coupon.find_coupon(coupon)
    payment = calculate_payment(cart_items, coupon)
    print(payment['total'])
    order_id = Order.add_order(current_user.id, payment["total"], coupon)
    Order.add_to_history(order_id, cart_items)
    User.updateBalanceWithdrawal(current_user.id, payment["total"])
    for item in cart_items:
        individualCost = calculate_payment([item], coupon)['subtotal']
        curBalance = float(User.get(item.seller_id).balance) + individualCost
        User.updateBalanceDeposit(item.seller_id, item.price * item.quantity)
        User.add_sold(item.seller_id, individualCost, datetime.datetime.now(), curBalance, item.product_name, item.quantity)
    Product.decrease_purchased_quantity(cart_items)
    Cart.clear_user_cart(current_user.id)
    return render_template('order_success.html', title='Order Success', user = User.get(current_user.id), order_id = order_id, cart_items = cart_items, payment = payment, coupon = coupon)

@bp.route('/checkout/apply-coupon', methods=['GET', 'POST'])
def apply_coupon():
    print("IM HERE")
    code = request.form['coupon'].upper()
    coupon = Coupon.find_coupon(code)
    if coupon is None:
        flash(f'The coupon code {code} is not valid!')
        print("KYS")
        return redirect(url_for('orders.checkout'))
    if Coupon.is_expired(code):
        flash(f'The coupon code {code} is not currently active!')
        print("WTF")
        return redirect(url_for('orders.checkout'))
    if coupon.product_id is not None:
        if not Cart.contains_item(current_user.id, coupon.product_id):
            flash(f'This coupon {code} is not applicable to an item in your cart!')
            print("QUE")
            return redirect(url_for('orders.checkout'))
    return redirect(url_for('orders.checkout', coupon = code))

