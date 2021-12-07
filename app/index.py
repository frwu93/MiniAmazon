from flask import render_template
from flask_login import current_user
import datetime
from flask import render_template, redirect, url_for, flash, request
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.testingDevon import Review
from .models.fulfill import Fulfill
from flask import current_app as app


from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l

from flask import Blueprint
bp = Blueprint('index', __name__)

ratingChoices=[(1,1), (2,2), (3,3), (4,4), (5,5)]
class ReviewForm(FlaskForm):
    #rating = IntegerField(_l('Product Rating'), validators=[DataRequired(), NumberRange(min=1, max=5, message="Please enter and integer between 1 and 5")])
    rating = SelectField(_l('Product Rating'), validators = [DataRequired()], choices=ratingChoices)    
    description = StringField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Leave Review'))


@bp.route('/')
def index(): 
    # get all available products for sale:
    #products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))

    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           purchase_history=purchases)


@bp.route('/product/<int:id>', methods = ["GET", "POST"])
def product(id):
    # get all available products for sale:
    print(id)
    form = ReviewForm()
    product = Product.get(id)
    quantity = request.args.get('quantity')
    print("HALLELUHAH")
    print(request.form.keys())
    print(type(quantity))
    review = Review.get_avg(id)
    if review==None:
        review=0
    if form.validate_on_submit():
        datetime.time
        Review.submitReview(current_user.id, id, form.rating.data, datetime.datetime.now() , form.description.data)     
        return render_template('product.html', product=product, review=review, form = form)
    else:
        if quantity:
            if int(quantity) > Product.get(id).quantity: 
                flash('This item is out of stock! Please wait until the seller restocks before purchasing.')
                return render_template('product.html', form = form,
                    product=product)
            success = Cart.add_to_cart(current_user.id, id, quantity)
            if success:
                return redirect(url_for('index.added_to_cart', id=id))
            else:
                flash('Could not add to cart. Check to see if you already have this item in your cart.')
                return render_template('product.html', form = form,
                    product=product)

        # find the products current user has bought:
        if product:
            return render_template('product.html',
                            product=product, review = review, form = form)
        else:
            return render_template('index.html',
                            avail_products= products,
                            purchase_history= purchases)


@bp.route('/product/addedToCart/<int:id>')
def added_to_cart(id):
    product = Product.get(id)
    return render_template('added_to_cart.html', product=product)


@bp.route('/products')
def products():
    return render_template('products.html')

@bp.route('/api/data')
def data():
    # get all available products for sale:
    available = True
    products = app.db.execute('''
SELECT *
FROM Products
WHERE available = :available
''',
                              available=available)
    

    myjson={}
    myjson["data"] = []
    for product in products:
        print(product.name)
        myjson["data"].append([product.id, product.name, product.price, product.imagelink])
    print(myjson)
    return(myjson)
    #return {
        #'data': [{'name': product.name, 'price': product.price, 'quantity': product.quantity} for product in products]
    #}