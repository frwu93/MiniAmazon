from flask import current_app as app
from flask import Flask
from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import date
from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, SearchForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm
from flask_ckeditor import CKEditor


##I am going to try and implement all of my stuff below here
class Review(newReview):
    def __init__(self, buyer_id, product_id, rating, time_reviewed, description):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.rating = rating
        self.time_reviewed = time_reviewed
        self.description= description

    @staticmethod
    def get(buyer_id, prdocut_id):
        rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE buyer_id = :buyer_id AND product_id = :product_id
''',
                              buyer_id=buyer_id, product_id = product_id)
        return Product_Rating(*(rows[0]), *(rows[1])) if rows is not None else None


    @staticmethod
    def submitReview(buyer_id, product_id, rating, time_reviewed, description):
        try:
            rows = app.db.execute("""
                INSERT INTO Product_Rating(buyer_id,product_id, rating, time_reviewed, lastname, description)
                VALUES(DEFAULT, :buyer_id, :password, :product_id, :rating, :time_reviewed, 0.0)
                RETURNING id
                """,
                                  buyer_id=buyer_id,
                                  product_id=product_id,
                                  rating=rating,
                                  time_reviewed=time_reviewed,
                                  description = description)
            buyer_id = rows[0][0]
            #print("backend reg; inserted into db")
            #print("Inserted: ", id)
            return None
        except Exception as e:
            print(e)
            # likely user already reviewed this
            # reporting needed
            print("not added")
            return None

ratingChoices=[(1,1), (2,2), (3,3), (4,4), (5,5)]
class ReviewForm(FlaskForm):
    rating = IntegerField(_l('Product Rating'), validators=[DataRequired(), NumberRange(min=1, max=5, message="Please enter and integer between 1 and 5")])
    #rating = SelectField(_l('Product Rating'), validators = [DataRequired()], choices=ratingChoices)    
    description = StringField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Leave Review'))



#@bp.route('/product/<int:id>', methods = ["Get", "Post"])
@bp.route('/later', methods = ["Get", "Post"])
def leaveReview():
    form = ReviewForm()
    if form.validate_on_submit():
        testingDevon.submitReview(current_user.id,     
                            ## add product ID,
                            id
                            form.rating.data,
                            form.request.args.get("time") 
                            form.description.data)
       return redirect(url_for(('messaging.post_review') ) ## CHANGE THIS)      
       return render_template('listItem.html', title='Sign In', form=form)




