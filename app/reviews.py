from flask import render_template
from flask_login import current_user
import datetime
from flask import render_template, redirect, url_for, flash, request
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.testingDevon import Review
from .models.product import Product
from .models.fulfill import Fulfill
from .models.user import User


from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from flask_login import current_user
import datetime

from .models.cart import Cart
from .models.product import Product
from flask import render_template, redirect, url_for, flash, request
from flask import Blueprint
bp = Blueprint('review', __name__)

ratingChoices=[(1,1), (2,2), (3,3), (4,4), (5,5)]

class UpdateForm(FlaskForm):
    #rating = IntegerField(_l('Product Rating'), validators=[DataRequired(), NumberRange(min=1, max=5, message="Please enter and integer between 1 and 5")])
    rating = SelectField(_l('Product Rating'), validators = [DataRequired()], choices=ratingChoices)    
    description = StringField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Update Review'))

class DeleteForm(FlaskForm):
    submit1 = SubmitField(_l('Delete Review'))



@bp.route('/product/reviews/<int:id>', methods = ["GET", "POST"])
def review_page(id):
    """[summary]
    Renders a product review page for the given product. Only allows a viewer to submit review if they have purchased the product. Allows users to view all product reviews 
    for given product, sorted based on rating reviews, and also allows users to delete/update current reviews. 
    Args:
        id ([type]): [int]

    Returns:
        [type]: [new template]
    """
    form = UpdateForm()
    form2=DeleteForm()
    getAvg=Review.get_avg(id)
    numReview=Review.get_Number(id)
    product=Product.get(id)
    reviews=Review.get_Reviews(id)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
        current_user_review = Review.current_user_review(current_user.id ,id)
    current_user_review = None
    if form.submit.data and form.validate_on_submit():
        Review.update_Review(current_user.id, id, form.rating.data, datetime.datetime.now() , form.description.data)
        return render_template('reviews.html', title='Review', numReview = numReview, getAvg = getAvg, product= product, reviews=reviews, current_user_review=current_user_review, form = form,
        form2 =form2)

    if form2.submit1.data and form2.validate_on_submit():
        Review.delete_Review(current_user.id, id)
        return render_template('reviews.html', title='Review', numReview = numReview, getAvg = getAvg, product= product, reviews=reviews, current_user_review=current_user_review, form = form,
        form2 =form2)
        
    return render_template('reviews.html', title='Review', numReview = numReview, getAvg = getAvg, product= product, reviews=reviews, 
    current_user_review=current_user_review, form = form, form2=form2)

### TAKING CARE OF SELLER BELOWS FROM HERE BELOW
### Function below no longer in use

