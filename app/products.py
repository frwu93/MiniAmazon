from flask import render_template
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request

import datetime

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)



@bp.route('/products/product/<int:id>')
def product(id):
    # get all available products for sale:
    product = Product.get(id)
    quantity = request.args.get('quantity')
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    if quantity: 
        success = Cart.add_to_cart(current_user.id, id, quantity)
        if success:
            return redirect(url_for('products.added_to_cart', id=id))
        else:
            flash('Could not add to cart. Check to see if you already have this item in your cart.')
            return render_template('product.html',
                product=product)
            

    # find the products current user has bought:
    if product:
        return render_template('product.html',
                        product=product)
    else:
        return render_template('products.html',
                           avail_products=allproducts,
                           purchase_history=purchases)

