from flask import current_app as app
from flask import render_template
from flask import Flask
from flask_login import current_user
import datetime
from flask import render_template, redirect, url_for, flash, request
from wtforms import StringField, IntegerField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
import time
 
from flask import Blueprint
#from flask_ckeditor import CKEditor
 
 
 
 
 
##I am going to try and implement all of my stuff below here
class Review:
   def __init__(self, buyer_id, product_id, rating, time_reviewed, description):
       """[summary]
Initalizes a Product Review Object
       Args:
           buyer_id (int): unique buyer id
           product_id (int): unique product id
           rating (int): product review rating
           time_reviewed (datetime): date at time of rating
           description (char[]): review description
       """
       self.buyer_id = buyer_id
       self.product_id = product_id
       self.rating = rating
       self.time_reviewed = time_reviewed
       self.description= description
 
   @staticmethod
   def get(buyer_id, product_id):
       """[summary]
    Returns all product ratings with these buyer_id and product_id
       Args:
           buyer_id (int): unique buyer id 
           product_id (int): unique product id 
       """
       rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE buyer_id = :buyer_id AND product_id = :product_id
''',
                             buyer_id=buyer_id, product_id = product_id)
       if rows:  
            return Review(*(rows[0]))
       else:
            return None
 
 
   @staticmethod
   def submitReview(buyer_id, product_id, rating, time_reviewed, description):
       try:
           rows = app.db.execute('''
               INSERT INTO Product_Rating(buyer_id,product_id, rating, time_reviewed, description)
               VALUES(:buyer_id, :product_id, :rating, :time_reviewed, :description)
               ''',
                                 buyer_id=buyer_id,
                                 product_id=product_id,
                                 rating=int(rating),
                                 time_reviewed=time_reviewed,
                                 description = description)
      
           return None
       except Exception as e:
           print(e)
           # likely user already reviewed this
           # reporting needed
           print("not added")
           return None

   @staticmethod
   def submitSellerReview(seller_id, buyer_id, rating, description, time_reviewed):
        """[summary]
        Submits a seller review for these given paramaters
       Args:
           seller_id (int): unique seller review
           buyer_id (int): unique buyer review
           rating (char[]): rating for review
           description (char[]): review description
           time_reviewed (datetime): current time
       """
        try:
           rows = app.db.execute("""
               INSERT INTO Seller_Rating(seller_id,buyer_id, rating, description, time_reviewed)
               VALUES(:seller_id, :buyer_id, :rating, :description, :time_reviewed)
               """,
                                 seller_id=seller_id,
                                 buyer_id=buyer_id,
                                 rating=int(rating),
                                 description=description,
                                 time_reviewed=time_reviewed)
      
           print("backend reg; inserted into db")
           return None
        except Exception as e:
           print(e)
           # likely user already reviewed this
           # reporting needed
           print("not added")
           return None
 
 
   @staticmethod
   def get_all(available=True):
       """[summary]
Finds all avaiable products, ordered by ID
       Args:
           available (bool, optional): Is the procut available. Defaults to True.
       """
       rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE available = :available
ORDER BY id
''',
                             available=available)
       return [Review(*row) for row in rows]
 
 
   @staticmethod
   def get_avg(product_id):
       """[summary]
Finds the average product review for a given product
       Args:
           product_id (int):  unique product id
       """
       rows = app.db.execute('''
SELECT AVG(rating)
FROM Product_Rating
WHERE product_id = :product_id
''', product_id=product_id
                             )
       if rows[0][0] is not None:
           return round((rows[0][0]), 2)
       return None



   @staticmethod
   def get_avgSeller(seller_id):
       """[summary]
Finds the average seller review for a given seller 
       Args:
           seller_id (int): unique seller id
       """
       rows = app.db.execute('''
SELECT AVG(rating)
FROM Seller_Rating
WHERE seller_id = :seller_id
''', seller_id=seller_id
                             )
       if rows[0][0] is not None:
           return round((rows[0][0]), 2)
       return None


   @staticmethod
   def get_Number(product_id):
       """[summary]
Finds the number of reviews a specific product has
       Args:
           product_id (int): unique product id
       """
       rows = app.db.execute('''
SELECT COUNT(rating)
FROM Product_Rating
WHERE product_id = :product_id
''', product_id=product_id
                             )
       return rows[0][0] if rows is not None else None

   @staticmethod
   def get_NumberSeller(seller_id):
       """[summary]
Finds the number of reviews a specific seller has
       Args:
           seller_id (int): unique seller id
       """
       rows = app.db.execute('''
SELECT COUNT(rating)
FROM Seller_Rating
WHERE seller_id = :seller_id
''', seller_id=seller_id
                             )
       if rows is not None:
           return rows[0][0]
       return 0


    
   @staticmethod
   def get_Reviews(product_id):
       """[summary]
Finds all reviews for a given product and returns them in descending rating order
       Args:
           product_id (int): unique product id
       """
       rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE product_id = :product_id
ORDER BY rating DESC
''', product_id=product_id
                             )
       return rows if rows is not None else None

   @staticmethod
   def get_UserReviews(buyer_id):
       """[summary]
Finds all product reviews a certain buyer has left
       Args:
           buyer_id (int): unique buyer id
       """
       rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE buyer_id = :buyer_id
ORDER BY time_reviewed DESC
''', buyer_id=buyer_id
                             )
    
       return rows if rows is not None else None
           



   @staticmethod
   def current_user_review(buyer_id, product_id):
       """[summary]
Finds the current users review for a specific product
       Args:
           buyer_id (int): unique buyer id
           product_id (int): unique product id
       """
       rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE product_id = :product_id AND buyer_id=:buyer_id
''', product_id=product_id, buyer_id=buyer_id
                             )
       if rows is not None and len(rows)>=1:
           return rows[0]
       return None








   @staticmethod
   def update_Review( buyer_id, product_id, rating, time_reviewed, description):
       """[summary]
Updates product review with the given parameters
       Args:
           buyer_id (int): unique buyer id
           product_id (int): unique product id
           rating (char): review to be updated
           time_reviewed (datetime): current time
           description (char[]): new review description

       Returns:
           [type]: [description]
       """
       
       try:
           app.db.execute('''
           UPDATE Product_Rating 
           SET buyer_id = :buyer_id, product_id = :product_id, rating = :rating, time_reviewed = :time_reviewed, description = :description 
           WHERE product_id = :product_id AND buyer_id = :buyer_id''', buyer_id=buyer_id, product_id=product_id, rating = int(rating), time_reviewed = time_reviewed, description = description)

       except Exception as e:
           print(e)
           print("Could not update value")
           return None
   @staticmethod
   def update_SellerReview(seller_id, buyer_id, rating, description, time_reviewed):
       """[summary]
Updates seller rating with the inputed paramters
       Args:
           seller_id (int): unique seller id
           buyer_id (int): unique buyer id
           rating (char): review to be updated
           description (char[]): current time
           time_reviewed (datetime): new review description

       Returns:
           None: 
       """
       try:
           app.db.execute('''
           UPDATE Seller_Rating 
           SET seller_id = :seller_id, buyer_id = :buyer_id, rating = :rating, description = :description, time_reviewed = :time_reviewed
           WHERE seller_id = :seller_id AND buyer_id = :buyer_id''', seller_id=seller_id, buyer_id=buyer_id, rating = int(rating), description = description , time_reviewed = time_reviewed)

       except Exception as e:
           print(e)
           print("Could not update value")
           return None


   @staticmethod
   def delete_Review(buyer_id, product_id):
       """[summary]
Deletes the product review for the given buyer and product
       Args:
           buyer_id (int): unique buyer id
           product_id (int): unique product id

       Returns:
           None: 
       """
       try:
           app.db.execute('''
           DELETE FROM Product_Rating 
           WHERE product_id = :product_id AND buyer_id = :buyer_id''', buyer_id=buyer_id, product_id=product_id)

       except Exception as e:
           print(e)
           print("Could not delete value")
           return None

   @staticmethod
   def delete_SellerReview(seller_id, buyer_id):
       """[summary]
Deletes the seller review for the given seller and buyer
       Args:
           seller_id (int): unique seller id
           buyer_id (int): unique buyer id

       Returns:
           None: 
       """
       try:
           app.db.execute('''
           DELETE FROM Seller_Rating 
           WHERE seller_id = :seller_id AND buyer_id = :buyer_id''', seller_id=seller_id, buyer_id=buyer_id)

       except Exception as e:
           print(e)
           print("Could not delete value")
           return None
   
   
   
   @staticmethod
   def get_Seller_Reviews(seller_id):
       """[summary]
Finds and returns the first review with this seller id
       Args:
           seller_id (int): unique seller id
       """
       rows = app.db.execute('''
SELECT *
FROM Seller_Rating
WHERE seller_id = :seller_id 
''', seller_id=seller_id
                             )
       if rows is not None and len(rows)>=1:
           return rows[0]
       return None

   @staticmethod
   def get_SellerReviews(seller_id):
       """[summary]
        Gets all reviews for this given seller
       Args:
           seller_id (int): unique seller id
       """
       rows = app.db.execute('''
SELECT *
FROM Seller_Rating
WHERE seller_id = :seller_id
ORDER BY time_reviewed DESC
''', seller_id=seller_id
                             )
    
       return rows if rows is not None else None

   @staticmethod
   def current_Seller_Review(buyer_id, seller_id):
       """[summary]
Finds this buyers review for the seller
       Args:
           buyer_id (int): unique buyer id
           seller_id (int): unique seller id
       """
       rows = app.db.execute('''
SELECT *
FROM Seller_Rating
WHERE seller_id = :seller_id AND buyer_id=:buyer_id
''', seller_id=seller_id, buyer_id=buyer_id
                             )
       if rows is not None and len(rows)>=1:
           return rows[0]
       return None


   @staticmethod
   def get_buyer_review_for_sellers(buyer_id):
       """[summary]
        Find all reviews this buyer has left for any seller 
       Args:
           buyer_id (int): unique buyer id
       """
       rows = app.db.execute('''
SELECT *
FROM Seller_Rating
WHERE buyer_id=:buyer_id
ORDER BY time_reviewed DESC
''', buyer_id=buyer_id
                             )
       if rows is not None and len(rows)>=1:
           return [row for row in rows]
       return None

       
                            
        
       


 
ratingChoices=[(1,1), (2,2), (3,3), (4,4), (5,5)]
class ReviewForm(FlaskForm):
   rating = IntegerField(_l('Product Rating'), validators=[DataRequired(), NumberRange(min=1, max=5, message="Please enter and integer between 1 and 5")])
   #rating = SelectField(_l('Product Rating'), validators = [DataRequired()], choices=ratingChoices)   
   description = StringField(_l('Description'), validators=[DataRequired()])
   submit = SubmitField(_l('Leave Review'))
 
 
 
#@bp.route('/product/<int:id>', methods = ["Get", "Post"])
#@bp.route('/later', methods = ["Get", "Post"])
#def leaveReview():
   #form = ReviewForm()
   #if form.validate_on_submit():
     #  testingDevon.submitReview(current_user.id,    
                           ## add product ID,
       #                    id,
      #                     form.rating.data,
        #                   form.request.args.get("time"),
        #                   form.description.data)
      # return redirect(url_for(('messaging.post_review') )   
   #return render_template('listItem.html', title='Sign In', form=form)
#




