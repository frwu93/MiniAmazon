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
import datetime
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
        print(email.data)
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))

    def validate_on_submit(self):
        try:           
            print(self.email.data)
            self.validate_email(self.email)        
        except:
            print("This email already has an account registered!") #change to flash later
            return False

            
        return True

        
@bp.route('/profile')
def profile():
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')
    address = request.args.get('address')
    password = request.args.get('password')
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
    
    user = User.get(current_user.id)
    return render_template('profile.html', title='Profile', user=user)


@bp.route('/register', methods=['GET', 'POST'])
def register():
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
            print('Congratulations, you are now a registered user!')

            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/paymentHistory', methods=['GET', 'POST'])
def paymentHistory():
    deposit = request.args.get('deposit')
    withdraw = request.args.get('withdraw')
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
    
    balance_history = Balance_History.get_balance_history_by_uid(current_user.id)
    user = User.get(current_user.id)
    return render_template('profile_subpages/payment_history.html', title='Payment', balance_history=balance_history, user=user)

@bp.route('/purchaseHistory', methods=['GET', 'POST'])
def purchaseHistory():
    purchase_history = Purchase_History.get_purchase_history_by_uid(current_user.id)
    user = User.get(current_user.id)
    return render_template('profile_subpages/purchase_history.html', title='Purchase', purchase_history=purchase_history, user=user)

@bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    user = User.get(current_user.id)
    reviews =  Review.get_UserReviews(current_user.id)
    sellerReviews=Review.get_SellerReviews(current_user.id)
    return render_template('profile_subpages/reviews.html', title='Reviews', user=user, reviews=reviews, sellerReviews=sellerReviews)

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    user = User.get(current_user.id)
    return render_template('profile_subpages/settings.html', title='Settings', user=user)

### ADDING THE REVIEW FORMS TO THE PAGE---NEED to create the forms first
class UpdateForms(FlaskForm):
    rating1 = SelectField(_l('Product Rating'), validators = [DataRequired()], choices=ratingChoices)    
    submit1 = SubmitField(_l('Submit Review'))
    description1= StringField(_l('Description'), validators=[DataRequired()])

class DeleteForms(FlaskForm):
    submit2 = SubmitField(_l('Delete Review'))

class LeaveForms(FlaskForm):
    rating3 = SelectField(_l('Product Rating'), validators = [DataRequired()], choices=ratingChoices)    
    submit3 = SubmitField(_l('Submit Review'))
    description3= StringField(_l('Description'), validators=[DataRequired()])


@bp.route('/user/<int:id>', methods=['GET', 'POST'])
def publicUser(id):
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

    ##boolean for whether or not you have bought an item from the seller 
    lst = Purchase_History.get_all_Sellers(current_user.id)
    print(lst)
    print("yo")
    myBool = False
    if id in lst:
        myBool=True

    if form.submit1.data and form.validate_on_submit:
        print(id, current_user.id, form.rating1.data, datetime.datetime.now())
        Review.update_SellerReview(id, current_user.id, form.rating1.data, form.description1.data, datetime.datetime.now())
        return render_template('public_user.html', title='Public User', user=user, form = form, 
        form2 = form2, current_user_review = current_user_review, reviews= reviews, getAvg= getAvg,numReview=numReview , form3=form3, myself=myself, myBool=myBool)

    if form3.submit3.data and form3.validate_on_submit:
        print("3")
        print((id, current_user.id, form3.rating3.data, datetime.datetime.now()))
        Review.submitSellerReview(id, current_user.id, form3.rating3.data, form3.description3.data, datetime.datetime.now())
        return render_template('public_user.html', title='Public User', user=user, form = form, 
        form2 =form2, current_user_review = current_user_review, reviews= reviews, getAvg= getAvg,numReview=numReview , form3=form3, myself=myself, myBool=myBool)

    if form2.submit2.data and form2.validate_on_submit():
        print("2")
        Review.delete_SellerReview(id, current_user.id)
        return render_template('public_user.html', title='Public User', user=user, form = form, 
        form2 =form2, current_user_review = current_user_review, reviews= reviews, getAvg= getAvg,numReview=numReview , form3=form3, myself=myself, myBool=myBool)

    print("4")
    return render_template('public_user.html', title='Public User', user=user, form = form, 
    form2 =form2, current_user_review = current_user_review, reviews= reviews, getAvg= getAvg,numReview=numReview, form3=form3 , myself=myself, myBool=myBool)

@bp.route('/user/<int:id>/products', methods=['GET', 'POST'])
def publicUserProducts(id):
    public_user_products = Public_User_Products.get_public_user_products_by_uid(id)
    user = User.get(id)
    return render_template('public_user_products.html', title='Public User Products', public_user_products=public_user_products, user=user)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

#<a href="{{ url_for('users.publicUser, id=selllerreview.seller_id) }}">View My Seller Page</a>
# <cite title="User"> </cite> You were rated {{ sellerreview.rating }} <cite> stars on  {{ sellerreview.time_reviewed }}</cite>