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
       self.buyer_id = buyer_id
       self.product_id = product_id
       self.rating = rating
       self.time_reviewed = time_reviewed
       self.description= description
 
   @staticmethod
   def get(buyer_id, product_id):
       rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE buyer_id = :buyer_id AND product_id = :product_id
''',
                             buyer_id=buyer_id, product_id = product_id)
       return (*(rows[0]), *(rows[1]) )if rows is not None else None
 
 
   @staticmethod
   def submitReview(buyer_id, product_id, rating, time_reviewed, description):
       try:
           rows = app.db.execute("""
               INSERT INTO Product_Rating(buyer_id,product_id, rating, time_reviewed, description)
               VALUES(:buyer_id, :product_id, :rating, :time_reviewed, :description)
               """,
                                 buyer_id=buyer_id,
                                 product_id=product_id,
                                 rating=int(rating),
                                 time_reviewed=time_reviewed,
                                 description = description)
      
           print("backend reg; inserted into db")
           #print("Inserted: ", id)
           return None
       except Exception as e:
           print(e)
           # likely user already reviewed this
           # reporting needed
           print("not added")
           return None

   @staticmethod
   def submitSellerReview(seller_id, buyer_id, rating, time_reviewed):
       try:
           rows = app.db.execute("""
               INSERT INTO Seller_Rating(seller_id,buyer_id, rating, time_reviewed)
               VALUES(:seller_id, :buyer_id, :rating, :time_reviewed)
               """,
                                 seller_id=seller_id,
                                 buyer_id=buyer_id,
                                 rating=int(rating),
                                 time_reviewed=time_reviewed)
      
           print("backend reg; inserted into db")
           #print("Inserted: ", id)
           return None
       except Exception as e:
           print(e)
           # likely user already reviewed this
           # reporting needed
           print("not added")
           return None
 
 
   @staticmethod
   def get_all(available=True):
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
       rows = app.db.execute('''
SELECT COUNT(rating)
FROM Product_Rating
WHERE product_id = :product_id
''', product_id=product_id
                             )
       return rows[0][0] if rows is not None else None

   @staticmethod
   def get_NumberSeller(seller_id):
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
       rows = app.db.execute('''
SELECT *
FROM Product_Rating
WHERE product_id = :product_id AND buyer_id=:buyer_id
''', product_id=product_id, buyer_id=buyer_id
                             )
       if rows is not None and len(rows)>=1:
           #print("hello", rows)
           return rows[0]
       return None








   @staticmethod
   def update_Review( buyer_id, product_id, rating, time_reviewed, description):
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
   def update_SellerReview(seller_id, buyer_id, rating, time_reviewed):
       try:
           app.db.execute('''
           UPDATE Seller_Rating 
           SET seller_id = :seller_id, buyer_id = :buyer_id, rating = :rating, time_reviewed = :time_reviewed
           WHERE seller_id = :seller_id AND buyer_id = :buyer_id''', seller_id=seller_id, buyer_id=buyer_id, rating = int(rating), time_reviewed = time_reviewed)

       except Exception as e:
           print(e)
           print("Could not update value")
           return None


   @staticmethod
   def delete_Review(buyer_id, product_id):
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
       rows = app.db.execute('''
SELECT *
FROM Seller_Rating
WHERE seller_id = :seller_id 
''', seller_id=seller_id
                             )
       if rows is not None and len(rows)>=1:
           #print("hello", rows)
           return rows[0]
       return None


   @staticmethod
   def current_Seller_Review(buyer_id, seller_id):
       rows = app.db.execute('''
SELECT *
FROM Seller_Rating
WHERE seller_id = :seller_id AND buyer_id=:buyer_id
''', seller_id=seller_id, buyer_id=buyer_id
                             )
       if rows is not None and len(rows)>=1:
           #print("hello", rows)
           return rows[0]
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




