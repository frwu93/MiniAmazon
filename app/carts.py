from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.product import Product
from .models.user import User
from flask import render_template, redirect, url_for, flash, request


from flask import Blueprint
bp = Blueprint('carts', __name__)



@bp.route('/cart', methods=['GET'])
def cart():
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
        cart_items = Cart.get_cart_products_by_uid(current_user.id) #TODO: make this goddamn fcn
        saved_items = Cart.get_saved_products_by_uid(current_user.id) #TODO: make this goddamn fcn
        payment = calculate_payment(cart_items)
    else:
        cart_items = None
    return render_template('cart.html', title='Cart', cart_items=cart_items, saved_items = saved_items, payment = payment)

@bp.route('/cart/changeQuantity/<int:buyer_id>-<int:product_id>-<int:quantity>-<int:page>')
@bp.route('/checkout/changeQuantity/<int:buyer_id>-<int:product_id>-<int:quantity>-<int:page>')
def changeQuantity(buyer_id, product_id, quantity, page):
    """
    Allows user to change quantity of item from either the cart page
    or the orders page

    Args:
        buyer_id (int): ID of user
        product_id (int): product ID of product being modified
        quantity (int): new quantity
        page (0,1): 0 if page requested from is carts page, 
        1 if page requested from is orders page

    Returns:
        Redirects back to either cart page or orders page, depending
        on which one the user was on
    """
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    Cart.change_quantity(buyer_id, product_id, quantity)
    if page == 1:
        return redirect(url_for('orders.checkout'))
    return  redirect(url_for('carts.cart'))

@bp.route('/cart/deleteItem/<int:buyer_id>-<int:product_id>')
def deleteItem(buyer_id, product_id):
    """
    Allows a user to delete an item from their cart

    Args:
        buyer_id (int): ID of user
        product_id (int): product ID of product being deleted
    Returns:
        Redirects to cart page
    """
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    deleted = Cart.delete_item(buyer_id, product_id)
    return redirect(url_for('carts.cart'))

@bp.route('/cart/move-to-cart/<int:buyer_id>-<int:product_id>')
def moveSavedItemToCart(buyer_id, product_id):
    """
    Moves a item in the user's "saved for later" list to the user's cart

    Args:
        buyer_id (int): ID of user
        product_id (int): product ID of product being moved

    Returns:

    Returns:
        Redirects to cart page
    """
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    Cart.toggle_saved(buyer_id, product_id)
    return redirect(url_for('carts.cart'))

@bp.route('/cart/add-to-cart/<int:buyer_id>-<int:product_id>-<int:quantity>')
def addToCart(buyer_id, product_id):
    """
    Allows a user to add an item to their cart

    Args:
        buyer_id (int): ID of user
        product_id (int): product ID of product being added to cart

    Returns:
        Redirect to cart page
    """
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    Cart.add_to_cart(buyer_id, product_id, quantity)
    return redirect(url_for('carts.cart'))

@bp.route('/cart/save-for-later/<int:buyer_id>-<int:product_id>')
def addToSaved(buyer_id, product_id):
    """
    Allows a user to add an item to their "saved for later" list

    Args:
       buyer_id (int): ID of user
        product_id (int): product ID of product being added to saved for later

    Returns:
        Redirects to cart page
    """
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    Cart.add_to_saved(buyer_id, product_id)
    return redirect(url_for('carts.cart'))

def calculate_payment(cart_items, coupon = None):
    """
    Calculates payment info for a transaction, including
    subtotal, tax, total, and savings (if a coupon is applied)

    Args:
        cart_items (list): List of items being bought
        coupon (Coupon, optional): Coupon being applied, if applicable. Defaults to None.

    Returns:
        dict: dictionary with payment info stored
    """
    subtotal = get_subtotal(cart_items)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    subtotal = get_subtotal(cart_items)
    saved = 0
    if coupon is not None:
        subtotal *= (1 - coupon.percent_off/100)
        saved = get_subtotal(cart_items) - subtotal 
        print(saved)
    tax = 0.03*subtotal
    total = subtotal + tax
    payment = {"subtotal": subtotal, "tax": tax,  "total":total, "saved":saved}
    return payment

    
def get_subtotal(cart : list) -> float:
    """
    Returns the subtotal of a list of items

    Args:
        cart (list): list of items in the cart

    Returns:
        float: subtotal of all items in the cart
    """
    total = 0
    for product in cart:
        total += float(product.order_cost)
    return total



