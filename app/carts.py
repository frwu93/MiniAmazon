from flask import render_template
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.product import Product
from flask import render_template, redirect, url_for, flash, request



from flask import Blueprint
bp = Blueprint('carts', __name__)


#api endpoints: checkout, delete item, change quantity, 

@bp.route('/cart', methods=['GET'])
def cart():
    print("go to cart")
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_products_by_uid(current_user.id) #TODO: make this goddamn fcn
        subtotal = Cart.get_subtotal(cart_items)
    else:
        cart_items = None
    return render_template('cart.html', title='Cart', cart_items=cart_items, subtotal = subtotal)

@bp.route('/cart/changeQuantity/<int:buyer_id>-<int:product_id>-<int:quantity>-<int:page>')
@bp.route('/checkout/changeQuantity/<int:buyer_id>-<int:product_id>-<int:quantity>-<int:page>')
def changeQuantity(buyer_id, product_id, quantity, page):
    print("Changing quantity of ", product_id, " to ", quantity)
    Cart.change_quantity(buyer_id, product_id, quantity)
    if page == 1:
        return redirect(url_for('orders.checkout'))
    return  redirect(url_for('carts.cart'))

@bp.route('/cart/deleteItem/<int:buyer_id>-<int:product_id>')
def deleteItem(buyer_id, product_id):
    print(f'Deleting item {product_id} from {buyer_id}\'s cart')
    deleted = Cart.delete_item(buyer_id, product_id)
    return redirect(url_for('carts.cart'))

    



