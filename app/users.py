from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from.models.testingDevon import Review
from .models.Purchase_History import Purchase_History
from .models.Balance_History import Balance_History
from.models.Public_User_Products import Public_User_Products
from .models.order import Order
from .models.coupon import Coupon


import datetime
from .carts import calculate_payment
from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange


from flask import Blueprint
bp = Blueprint('users', __name__)

ratingChoices=[(1,1), (2,2), (3,3), (4,4), (5,5)]

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))




@bp.route('/login', methods=['GET', 'POST'])
def login():
    """[summary]
    Attempts to login user into the site
    Returns:
        render_template: redirects to the next page if successful, otherwise remains on login
    """
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        """[summary]
        Checks to see if the email is already in use
        Args:
            email (String): the email the user attempts to register with

        Raises:
            ValidationError: will be returned if email already in use
        """
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))

    def validate_on_submit(self):
        """[summary]
        Checks to see if email is already use when user submits registration
        Returns:
            boolean: whether email is used or not
        """
        try:           
            self.validate_email(self.email)        
        except:
            flash("This email already has an account registered!")
            return False

            
        return True

        
@bp.route('/profile')
def profile():
    """[summary]
    Route when user goes to their profile page
    Returns:
        render_template: redirects user to the profile page
    """
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')
    address = request.args.get('address')
    password = request.args.get('password')
    profilepic = request.args.get('profilepic')
    if firstname:
        id = User.updateFirstName(current_user.id, firstname)
    if lastname:
        id = User.updateLastName(current_user.id, lastname)
    if email:
        id = User.updateEmail(current_user.id, email)
    if address:
        id = User.updateAddress(current_user.id, address)
    if password:
        id = User.updatePassword(current_user.id, password)
    if profilepic:
        id = User.updateProfilePic(current_user.id, profilepic)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    user = User.get(current_user.id)
    return render_template('profile.html', title='Profile', user=user)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """[summary]
    Attempts to register user
    Returns:
        redirect: redirects to login page if successful registration
        render_template: reamins on register page if unsuccessful registration
    """
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
            flash('Congratulations, you are now a registered user!')

            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/paymentHistory', methods=['GET', 'POST'])
def paymentHistory():
    """[summary]
    Route when user goes to their payment/balance page
    Returns:
        render_template: renders the balance/payment html page
    """
    deposit = request.args.get('deposit')
    withdraw = request.args.get('withdraw')
    profilepic = request.args.get('profilepic')
    if deposit:
        id = User.updateBalanceDeposit(current_user.id, deposit)
        curBalance = User.get(current_user.id).balance
        User.add_deposit(current_user.id, deposit, datetime.datetime.now(), curBalance)
        return redirect(url_for('users.paymentHistory'))
    if withdraw:
        id = User.updateBalanceWithdrawal(current_user.id, withdraw)
        curBalance = User.get(current_user.id).balance
        User.add_withdrawal(current_user.id, withdraw, datetime.datetime.now(), curBalance)
        return redirect(url_for('users.paymentHistory'))
    if profilepic:
        id = User.updateProfilePic(current_user.id, profilepic)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    balance_history = Balance_History.get_balance_history_by_uid(current_user.id)
    user = User.get(current_user.id)
    return render_template('profile_subpages/payment_history.html', title='Payment', balance_history=balance_history, user=user)

@bp.route('/purchaseHistory', methods=['GET', 'POST'])
def purchaseHistory():
    """[summary]
    Route when user goes to their purchase history page
    Returns:
        render_template: renders the purchase history html page
    """
    profilepic = request.args.get('profilepic')
    if profilepic:
        id = User.updateProfilePic(current_user.id, profilepic)
    purchase_history = Purchase_History.get_purchase_history_by_uid(current_user.id)
    user = User.get(current_user.id)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    return render_template('profile_subpages/purchase_history.html', title='Purchase', purchase_history=purchase_history, user=user)

@bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    """[summary]
    Route when user goes to their reviews page
    Returns:
        render_template: renders the reviews html page
    """
    profilepic = request.args.get('profilepic')
    if profilepic:
        id = User.updateProfilePic(current_user.id, profilepic)
    user = User.get(current_user.id)
    reviews =  Review.get_UserReviews(current_user.id)
    sellerReviews=Review.get_SellerReviews(current_user.id)
    reviews4seller=Review.get_buyer_review_for_sellers(current_user.id)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    if reviews4seller is None:
        return render_template('profile_subpages/reviews.html', title='Reviews', user=user, reviews=reviews, sellerReviews=sellerReviews)
    return render_template('profile_subpages/reviews.html', title='Reviews', user=user, reviews=reviews, sellerReviews=sellerReviews, reviews4seller=reviews4seller)

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """[summary]
    Route when user goes to their settings page
    Returns:
        render_template: renders the setttings html page
    """
    profilepic = request.args.get('profilepic')
    if profilepic:
        id = User.updateProfilePic(current_user.id, profilepic)
    user = User.get(current_user.id)
    is_seller = User.isSeller(current_user.id)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    return render_template('profile_subpages/settings.html', title='Settings', user=user, is_seller=is_seller)

@bp.route('/settings/newSeller/<int:id>')
def add_user_to_seller(id):
    """[summary]
    This function adds the user to the seller table when they register for it in settigns
    Args:
        id (integer): the id of the user who want's to become a seller

    Returns:
        redirect: link back to the user's settings page
    """
    User.updateSellers(id)
    return redirect(url_for('users.settings'))

### ADDING THE REVIEW FORMS TO THE PAGE---NEED to create the forms first
class UpdateForms(FlaskForm):
    rating1 = SelectField(_l('Rating'), validators = [DataRequired()], choices=ratingChoices)    
    submit1 = SubmitField(_l('Submit Review'))
    description1= StringField(_l('Description'), validators=[DataRequired()])

class DeleteForms(FlaskForm):
    submit2 = SubmitField(_l('Delete Review'))

class LeaveForms(FlaskForm):
    rating3 = SelectField(_l('Rating'), validators = [DataRequired()], choices=ratingChoices)    
    submit3 = SubmitField(_l('Submit Review'))
    description3= StringField(_l('Description'), validators=[DataRequired()])


@bp.route('/user/<int:id>', methods=['GET', 'POST'])
def publicUser(id):
    """[summary]
    Route to each user's public view page
    Args:
        id (integer): id of the user we want to see

    Returns:
        render_template: renders the public user view html page
    """
    if not current_user.is_authenticated:
        flash('Log in to view a user profile!')
        return redirect( url_for('index.index'))
        
    form = UpdateForms()
    form2=DeleteForms()
    form3=LeaveForms()
    current_user_review=Review.current_Seller_Review(current_user.id, id)
    reviews=Review.get_Seller_Reviews(id)
    user = User.get(id)
    getAvg=Review.get_avgSeller(id)
    numReview=Review.get_NumberSeller(id)
    myself = True
    if (current_user.id==id):
        myself=False
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    ##boolean for whether or not you have bought an item from the seller 
    lst = Purchase_History.get_all_Sellers(current_user.id)
    myBool = False
    if id in lst:
        myBool=True

    if form.submit1.data and form.validate_on_submit:
        Review.update_SellerReview(id, current_user.id, form.rating1.data, form.description1.data, datetime.datetime.now())
        return redirect(url_for('users.publicUser', id=id))
    if form3.submit3.data and form3.validate_on_submit:
        Review.submitSellerReview(id, current_user.id, form3.rating3.data, form3.description3.data, datetime.datetime.now())
        return redirect(url_for('users.publicUser', id=id))

    if form2.submit2.data and form2.validate_on_submit():
        Review.delete_SellerReview(id, current_user.id)
        return redirect(url_for('users.publicUser', id=id))

    return render_template('public_user.html', title='Public User', user=user, form = form, 
    form2 =form2, current_user_review = current_user_review, reviews= reviews, getAvg= getAvg,numReview=numReview, form3=form3 , myself=myself, myBool=myBool)

@bp.route('/user/<int:id>/products', methods=['GET', 'POST'])
def publicUserProducts(id):
    """[summary]
    Route to the public user view's product page
    Args:
        id (integer): the id of the seller

    Returns:
        render_template: renders the public user view products html page
    """
    public_user_products = Public_User_Products.get_public_user_products_by_uid(id)
    user = User.get(id)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    return render_template('public_user_products.html', title='Public User Products', public_user_products=public_user_products, user=user)

@bp.route('/user/order/<int:order_id>', methods=['GET', 'POST'])
def order_confirmation(order_id):
    """[summary]
    Route to the order confirmation page for each order in the purchase history profile page
    Args:
        order_id (integer): id of the order we are viewing

    Returns:
        render_template: renders the order_confirmation html page
    """
    purchased_items = Purchase_History.get_purchase_history_by_order_id(order_id)
    coupon_code = Order.get_coupon(order_id)
    coupon = Coupon.find_coupon(coupon_code)
    payment = calculate_payment(purchased_items, coupon)
    if current_user.is_authenticated:
        if (User.isSeller(current_user.id)):
            current_user.isSeller = True
        else:
            current_user.isSeller = False
    return render_template('order_success.html', title='Order Success', user = User.get(current_user.id), order_id = order_id, cart_items = purchased_items, payment = payment, coupon = coupon)

@bp.route('/logout')
def logout():
    """[summary]
    Route to logout the user
    Returns:
        redirect: redirects back to the home page when user is not logged in
    """
    logout_user()
    return redirect(url_for('index.index'))

#<a href="{{ url_for('users.publicUser, id=selllerreview.seller_id) }}">View My Seller Page</a>
# <cite title="User"> </cite> You were rated {{ sellerreview.rating }} <cite> stars on  {{ sellerreview.time_reviewed }}</cite>