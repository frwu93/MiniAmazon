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


from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l

from flask import Blueprint
bp = Blueprint('filter', __name__)


class FilterForm(FlaskForm):
    categories = ['All', 'Automotives', 'Accessories', 'Books', 'Beauty', 'Clothing', 'Entertainment', 'Electronics', 'Food', 'Home', 'Outdoors', 'Pet Supplies', 'Sports', 'Toys', 'Other']
    minprice = DecimalField(_l('List Price'), validators=[NumberRange(min=0, message="Price must be nonnegative")])
    maxprice = DecimalField(_l('List Price'), validators=[NumberRange(min=minprice, message="Price must be nonnegative")])
    minStars = DecimalField(_l('List Price'), validators=[NumberRange(min=0, max=5, message="Price must be nonnegative")])
    submit = SubmitField(_l('List Item'))

@bp.route('/filter', methods=['POST'])
def filter(): 
    # get all available products for sale:
    print(request.form['categories'])
    print(request.form['rating'])
    print(request.form['minPrice'])
    print(request.form['maxPrice'])


    category = request.form['categories']
    rating = request.form['rating']
    if request.form['minPrice']:
        minP = request.form['minPrice']
        print(minP)
        print("Big whoops")
    else:
        print("No min")
        minP = 0
    minP = int(minP)
    if request.form['maxPrice']:
        maxP = request.form['maxPrice']
    else:
        maxP = 10000000000
    maxP = int(maxP)

    if(minP > maxP):
        flash('Min price must be less than max price!')
        return redirect(url_for('index.products'))

    print(minP)
    return redirect(url_for('filter.filterResults', category=category, rating=rating, min=minP, max=maxP))


@bp.route('/filter/result/<string:category>/<int:rating>/<float:min>/<float:max>/')
def filterResults(category, rating, min, max): 
    products = Product.filter(category, rating, min, max, True)
    
    #for product in products:
     #   product.rating = Review.get_avg(product.id)
    if products:
        return render_template('filter.html', avail_products = products)
    else:
        return redirect(url_for('index.index'))








