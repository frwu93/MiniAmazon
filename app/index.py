from flask import render_template
from flask_login import current_user
import datetime
from flask import render_template, redirect, url_for, flash, request

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))

    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)

@bp.route('/product/<int:id>')
def product(id):
    # get all available products for sale:
    product = Product.get(id)
    quantity = request.args.get('quantity')
    print("HALLELUHAH")
    print(quantity)
    print(type(quantity))
    if quantity is not None:
        if int(quantity) <= Product.get(id).quantity: 
            success = Cart.add_to_cart(current_user.id, id, quantity)
            if success:
                return redirect(url_for('index.added_to_cart', id=id))
            else:
                flash('Could not add to cart. Check to see if you already have this item in your cart.')
                return render_template('product.html',
                    product=product)
        else:
            flash('This item is out of stock! Please wait until the seller restocks before purchasing.')

          

    # find the products current user has bought:
    if product:
        return render_template('product.html',
                        product=product)
    else:
        return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)


@bp.route('/product/addedToCart/<int:id>')
def added_to_cart(id):
    product = Product.get(id)
    return render_template('added_to_cart.html', product=product)

