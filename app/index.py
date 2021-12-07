from flask import render_template
from flask_login import current_user
import datetime
from flask import render_template, redirect, url_for, flash, request
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.Purchase_History import Purchase_History
from .models.testingDevon import Review
from .models.fulfill import Fulfill
from .models.user import User
from flask import current_app as app

from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, Required
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l

from flask import Blueprint
bp = Blueprint('index', __name__)

ratingChoices=[(1,1), (2,2), (3,3), (4,4), (5,5)]
#This is the review form that has rating and description
class ReviewForm(FlaskForm):
    #rating = IntegerField(_l('Product Rating'), validators=[DataRequired(), NumberRange(min=1, max=5, message="Please enter and integer between 1 and 5")])
    rating = SelectField(_l('Product Rating'), validators = [DataRequired()], choices=ratingChoices)    
    description = StringField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Leave Review'))


#This is the edit product form that has new fields to edit

class EditForm(FlaskForm):
    categories = ['Automotives', 'Accessories', 'Books', 'Beauty', 'Clothing', 'Entertainment', 'Electronics', 'Food', 'Home', 'Outdoors', 'Pet Supplies', 'Sports', 'Toys', 'Other']
    productName = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    imageLink = StringField(_l('Image Link'), validators=[DataRequired()])
    category = SelectField(u'Category', choices = categories, validators = [Required()])
    submit = SubmitField(_l('Edit'))


#This is our home page
@bp.route('/')
def index(): 
    # get best and top products for sale:
    BestSellingProducts = Product.get_best_selling(True)
    TopRatedProducts = Product.get_top_rated(True)

    #This is to verify that user is or is not seller, used almost everywhere to only display inventory if seller
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
        print(current_user.isSeller)

    else:
        purchases = None

    # render the page by adding information to the index3.html file
    return render_template('index3.html',
                           purchase_history=purchases,
                           avail_products = BestSellingProducts,
                           top_rated = TopRatedProducts)


#product page
@bp.route('/product/<int:id>', methods = ["GET", "POST"])
def product(id):

    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False

    form = ReviewForm()
    product = Product.get(id)

    #Should only show when form is submitted to checkout some quantity
    quantity = request.args.get('quantity')
    review = Review.get_avg(id)
    myBool=False
    lst=Purchase_History.get_product_names(current_user.id)

    #Verifies that you have bought this product so you can leave a review
    if product.name in lst:
        myBool=True
    print(myBool)
    myreview = Review.get(current_user.id, id)
    if review==None:
        review=0

    #If you fill out review form, refresh and added review to database
    if form.validate_on_submit():
        datetime.time
        Review.submitReview(current_user.id, id, form.rating.data, datetime.datetime.now() , form.description.data)     
        return redirect(url_for('index.product', id=id))


    else:
        #If you attempt to check out
        if quantity:
            if int(quantity) > Product.get(id).quantity: 
                flash('This item is out of stock! Please wait until the seller restocks before purchasing.')
                return render_template('product.html', form = form,
                    product=product, myreview = myreview)
            success = Cart.add_to_cart(current_user.id, id, quantity)
            if success:
                return redirect(url_for('index.added_to_cart', id=id))
            else:
                flash('Could not add to cart. Check to see if you already have this item in your cart.')
                return render_template('product.html', form = form,
                    product=product, myreview = myreview)

        # else
        if product:
            return render_template('product.html',
                            product=product, review = review, form = form, myreview = myreview, myBool=myBool)
        else:
            return render_template('index.html',
                            avail_products= products,
                            purchase_history= purchases)


#Added product to cart confirmation
@bp.route('/product/addedToCart/<int:id>')
def added_to_cart(id):
    product = Product.get(id)
    return render_template('added_to_cart.html', product=product)


#Full product gallery
@bp.route('/products')
def products():
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    return render_template('products.html')

#Edit product form page, redirects to product page upon completion
@bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def productEdit(id):
    form = EditForm()
    product = Product.get(id)
    curr_name = product.name
    curr_imageLink = product.imageLink
    curr_description = product.description
    if form.validate_on_submit():
        Product.editInfo(id,
                            form.productName.data,
                            form.description.data,
                            form.imageLink.data,
                            form.category.data)
        return redirect(url_for('index.product', id = id))
    return render_template('product_edit.html', form=form, curr_name=curr_name, curr_imageLink = curr_imageLink, curr_description=curr_description)


#Api call to get data for every product for sale
@bp.route('/api/data')
def data():
    # get all available products for sale, database query here so we don't have to cast all to Products (takes too much time)
    available = True
    products = app.db.execute('''
SELECT products.id, name, price, imageLink, avg(rating) 
FROM (products left join product_rating on products.id=product_rating.product_id) 
WHERE available = TRUE
group by products.id ORDER BY avg DESC NULLS LAST
''',
                              available=available)
    
    #Add data to JSON payload
    myjson={}
    myjson["data"] = []
    for product in products:
        if product.avg:
            rating = float(round(product.avg, 2))
        else:
            rating = 0.00
        myjson["data"].append([product.id, product.name, product.price, product.imagelink, "{:.2f}".format(rating)])
    return(myjson)