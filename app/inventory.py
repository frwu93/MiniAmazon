from flask import render_template
from flask_login import current_user
import datetime

from flask import render_template, redirect, url_for, flash, request
from .models.product import Product
from .models.purchase import Purchase
from .models.fulfill import Fulfill
from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, Required
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l


import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


from flask import Blueprint
bp = Blueprint('inventory', __name__)



class ProductForm(FlaskForm):
    categories = ['Automotives', 'Accessories', 'Books', 'Beauty', 'Clothing', 'Entertainment', 'Electronics', 'Food', 'Home', 'Outdoors', 'Pet Supplies', 'Sports', 'Toys', 'Other']
    productName = StringField(_l('Product Name'), validators=[DataRequired()])
    quantity = IntegerField(_l('Quantity'), validators=[DataRequired(), NumberRange(min=1, message="Quantity must be at least 1")])
    description = StringField(_l('Description'), validators=[DataRequired()])
    imageLink = StringField(_l('Image Link'), validators=[DataRequired()])
    category = SelectField(u'Category', choices = categories, validators = [Required()])
    price = DecimalField(_l('List Price'), validators=[DataRequired(), NumberRange(min=0, message="Price must be nonnegative")])
    submit = SubmitField(_l('List Item'))


@bp.route('/inventory')
def inventory():
    # get all available products for sale:
    print("go to inventory")
    products = Product.get_all_by_seller(current_user.id, True)
    args = request.args
    for i in args.keys():
        print(i, " whoops")
        mylist = i.split("-")
        order_id = mylist[1]
        product_id = mylist[2]
        Fulfill.fulfill(order_id, product_id)
        
    # find the products current user has bought:
    if current_user.is_authenticated:
        fulfill = Fulfill.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        fulfill = None
    return render_template('inventory.html',
                           avail_products=products,
                           order_fulfill=fulfill)

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

@bp.route('/analytics')
def analytics():
    # get all available products for sale:
    fulfill = Fulfill.get_all_by_uid_since_reverseOrder(
        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    
    data = {}
    numberSold = {}
    for item in fulfill:
        year, month = item.time_ordered.year, item.time_ordered.month
        month = str(year) + "/" + str(month)
        if month not in data.keys():
            data[month] = 0
        data[month] += item.quantity

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
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Total products sold over time")
    axis.set_xlabel("date")
    axis.set_yticks(np.arange(np.min(totalSold), np.max(totalSold), round(int((np.max(totalSold) - np.min(totalSold))/10)/10)*10))
    axis.set_ylabel("total products sold")

    axis.plot(data.keys(), totalSold, "ro-")

    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    c=Counter(numberSold)
    mostCommon = c.most_common()


    return render_template('analytics.html', image=pngImageB64String, mostCommon = mostCommon)
    #return render_template('analytics.html', name = 'new_plot', url ='/static/images/new_plot.png')

@bp.route('/deleteItem/<int:id>')
def deleteItem(id):
    # get all available products for sale:
    print("Removing  item: ", id)

    product = Product.remove_listing(id)
    return redirect(url_for('inventory.inventory'))

@bp.route('/inventory/changeQuantity/<int:id>-<int:quantity>')
def changeQuantity(id, quantity):
    # get all available products for sale:
    print("Changing quantity of ", id, " to ", quantity)
    product = Product.change_quantity(id, quantity)
    return redirect(url_for('inventory.inventory'))

@bp.route('/inventory/changePrice/<int:id>-<float:price>')
def changePrice(id, price):
    # get all available products for sale:
    print("Changing price of ", id, " to ", price)
    product = Product.change_price(id, price)
    return redirect(url_for('inventory.inventory'))


