from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.product import Product
from .models.user import User
from flask import render_template, redirect, url_for, flash, request



from flask import Blueprint
bp = Blueprint('carts', __name__)


#api endpoints: checkout, delete item, change quantity, 

@bp.route('/cart', methods=['GET'])
def cart():
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    print("go to cart")
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id) #TODO: make this goddamn fcn
        saved_items = Cart.get_saved_products_by_uid(current_user.id) #TODO: make this goddamn fcn
        payment = calculate_payment(cart_items)
    else:
        cart_items = None
    return render_template('cart.html', title='Cart', cart_items=cart_items, saved_items = saved_items, payment = payment)

@bp.route('/cart/changeQuantity/<int:buyer_id>-<int:product_id>-<int:quantity>-<int:page>')
@bp.route('/checkout/changeQuantity/<int:buyer_id>-<int:product_id>-<int:quantity>-<int:page>')
def changeQuantity(buyer_id, product_id, quantity, page):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    print("Changing quantity of ", product_id, " to ", quantity)
    Cart.change_quantity(buyer_id, product_id, quantity)
    if page == 1:
        return redirect(url_for('orders.checkout'))
    return  redirect(url_for('carts.cart'))

@bp.route('/cart/deleteItem/<int:buyer_id>-<int:product_id>')
def deleteItem(buyer_id, product_id):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    print(f'Deleting item {product_id} from {buyer_id}\'s cart')
    deleted = Cart.delete_item(buyer_id, product_id)
    return redirect(url_for('carts.cart'))

@bp.route('/cart/move-to-cart/<int:buyer_id>-<int:product_id>')
def moveSavedItemToCart(buyer_id, product_id):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    Cart.toggle_saved(buyer_id, product_id)
    return redirect(url_for('carts.cart'))

@bp.route('/cart/add-to-cart/<int:buyer_id>-<int:product_id>-<int:quantity>')
def addToCart(buyer_id, product_id):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    Cart.add_to_cart(buyer_id, product_id, quantity)
    return redirect(url_for('carts.cart'))

@bp.route('/cart/save-for-later/<int:buyer_id>-<int:product_id>')
def addToSaved(buyer_id, product_id):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    Cart.add_to_saved(buyer_id, product_id)
    return redirect(url_for('carts.cart'))

def calculate_payment(cart_items, coupon = None):
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    subtotal = Cart.get_subtotal(cart_items)
    saved = 0
    if coupon is not None:
        subtotal *= (1 - coupon.percent_off/100)
        saved = Cart.get_subtotal(cart_items) - subtotal 
        print(saved)
    tax = 0.03*subtotal
    total = subtotal + tax
    payment = {"subtotal": subtotal, "tax": tax,  "total":total, "saved":saved}
    return payment



