from flask import render_template
from flask_login import current_user
import datetime

from flask import render_template, redirect, url_for, flash, request
from .models.product import Product
from .models.purchase import Purchase
from .models.coupon import Coupon
from .models.fulfill import Fulfill
from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, Required, Length
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l


import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import AutoDateFormatter, AutoDateLocator

from collections import Counter


from flask import Blueprint
bp = Blueprint('inventory', __name__)


#Forms for listing a product and creating a coupon
class ProductForm(FlaskForm):
    categories = ['Automotives', 'Accessories', 'Books', 'Beauty', 'Clothing', 'Entertainment', 'Electronics', 'Food', 'Home', 'Outdoors', 'Pet Supplies', 'Sports', 'Toys', 'Other']
    productName = StringField(_l('Product Name'), validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[DataRequired(), NumberRange(min=1, message="Quantity must be at least 1")])
    #quantity = SelectField(_l('Quantity'), validators = [DataRequired()], choices=[(1,"Group1"),(2,"Group2")])    
    description = StringField(_l('Description'), validators=[DataRequired()])
    imageLink = StringField(_l('Image Link'), validators=[DataRequired()])
    category = SelectField(u'Category', choices = categories, validators = [Required()])
    price = DecimalField(_l('List Price'), validators=[DataRequired(), NumberRange(min=0, message="Price must be nonnegative")])
    submit = SubmitField(_l('List Item'))

class CouponForm(FlaskForm):
    percentOff = DecimalField(_l('Percent Off'), validators=[DataRequired(), NumberRange(min=1, max=100, message="Percent Off must be from 1-100")])
    couponCode = StringField(_l('Coupon Code'), validators=[DataRequired(), Length(max=10)])
    start = DateField('Start Date', format='%m/%d/%Y')
    end = DateField('End Date', format='%m/%d/%Y')
    submit = SubmitField(_l('Create Coupon'))



#Inventory page foor seller
@bp.route('/inventory')
def inventory():
    # get all available your products for sale:
    products = Product.get_all_by_seller(current_user.id, True)
    args = request.args

    #Check which items to fulfill
    for i in args.keys():
        if i.startswith("fulfill"):
            mylist = i.split("-")
            order_id = mylist[1]
            product_id = mylist[2]
            Fulfill.fulfill(order_id, product_id)
        
    # find all orders of your products
    if current_user.is_authenticated:
        fulfill = Fulfill.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        fulfill = None
    return render_template('inventory.html',
                           avail_products=products,
                           order_fulfill=fulfill)


#List a new item form redirect
@bp.route('/sellItem', methods=['GET', 'POST'])
def sellItem():
    form = ProductForm()
    if form.validate_on_submit():
        Product.new_listing(current_user.id,
                            form.productName.data,
                            form.quantity.data,
                            form.description.data,
                            form.imageLink.data,
                            form.category.data,
                            form.price.data)
        return redirect(url_for('inventory.inventory'))
    return render_template('listItem.html', title='Sign In', form=form)


#Page for your analytics
@bp.route('/analytics')
def analytics():
    fulfill = Fulfill.get_all_by_uid_since_reverseOrder(
        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    
    data = {}
    numberSold = {}
    #Get number sold of each item and date
    for item in fulfill:
       

        date = item.time_ordered.date()
        if date not in data.keys():
            data[date] = 0
        data[date] += item.quantity


        product = item.name
        quantity = item.quantity
        if product not in numberSold.keys():
            numberSold[product] = 0
        numberSold[product] += quantity

    totalSold = []
    sum = 0
    for k in data.values():
        sum += k
        totalSold.append(sum)

    #Create graph
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Total products sold over time")
    axis.set_xlabel("date")
    axis.set_ylabel("total products sold")
    
    axis.plot(data.keys(), totalSold)

    axis.tick_params(axis='x', labelrotation = -45)
    fig.tight_layout()


    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')


    #Most commonly sold items
    c=Counter(numberSold)
    mostCommon = c.most_common()


    return render_template('analytics.html', image=pngImageB64String, mostCommon = mostCommon)

#Deletes item
@bp.route('/deleteItem/<int:id>')
def deleteItem(id):
    # get all available products for sale:
    product = Product.remove_listing(id)
    return redirect(url_for('inventory.inventory'))


#Change quantity of item
@bp.route('/inventory/changeQuantity/<int:id>-<int:quantity>')
def changeQuantity(id, quantity):
    # get all available products for sale:
    product = Product.change_quantity(id, quantity)
    return redirect(url_for('inventory.inventory'))

#Change price of item
@bp.route('/inventory/changePrice/<int:id>-<float:price>')
def changePrice(id, price):
    # get all available products for sale:
    product = Product.change_price(id, price)
    return redirect(url_for('inventory.inventory'))

#Add coupon for some item
@bp.route('/addCoupon/<int:id>', methods=['GET', 'POST'])
def addCoupon(id):
    form = CouponForm()
    if form.validate_on_submit():
        Coupon.new_coupon(form.couponCode.data,
                             form.percentOff.data,
                             form.start.data,
                             form.end.data,
                             id)
        return redirect(url_for('inventory.inventory'))
    return render_template('create_coupon.html', form = form, id = id)
