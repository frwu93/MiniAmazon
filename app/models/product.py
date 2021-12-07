from flask import current_app as app
from flask import Flask
from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from .testingDevon import Review

class Product:
    def __init__(self, id, seller_id, name, description, imageLink, category, price, available, quantity):
        self.id = id
        self.seller_id = seller_id
        sellerName = self.get_seller_name(self.seller_id)
        self.seller_name = sellerName[0] + " " + sellerName[1]
        self.name = name
        self.description = description
        self.imageLink = imageLink
        self.category = category
        self.price = '{:.2f}'.format(price)
        self.available = available
        self.quantity = quantity
        if Review.get_avg(id):
            self.rating = Review.get_avg(id)
        else:
            self.rating = 0

    @staticmethod
    def get_seller_name(id):
        rows = app.db.execute('''
SELECT firstname, lastname
FROM Users
WHERE id = :id
''',
                              id=id)
        return rows[0]

    @staticmethod
    def get_seller_name(id):
        rows = app.db.execute('''
SELECT firstname, lastname
FROM Users
WHERE id = :id
''',
                              id=id)
        return rows[0]

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def filter(category, rating, min, max, available=True):
        if rating != 0:
            if category != "All":
                rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        AND category = :category
        AND price <= :max
        AND price >= :min
        ORDER BY id
        ''',
                                    available=available,
                                    category=category,
                                    min=min,
                                    max=max)
                return [Product(*row) for row in rows if (Review.get_avg(row[0]) and Review.get_avg(row[0]) >= rating)]
            else:
                rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        AND price <= :max
        AND price >= :min
        ORDER BY id
        ''',
                                    available=available,
                                    min=min,
                                    max=max)
                for row in rows:
                    print(row[0])
                return [Product(*row) for row in rows if (Review.get_avg(row[0]) and Review.get_avg(row[0]) >= rating)]
        else:
            if category != "All":
                rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        AND category = :category
        AND price <= :max
        AND price >= :min
        ORDER BY id
        ''',
                                    available=available,
                                    category=category,
                                    min=min,
                                    max=max)
                for row in rows:
                    print(row[0])
                return [Product(*row) for row in rows]
            else:
                rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE available = :available
        AND price <= :max
        AND price >= :min
        ORDER BY id
        ''',
                                    available=available,
                                    min=min,
                                    max=max)
                for row in rows:
                    print(row[0])
                return [Product(*row) for row in rows]

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE available = :available
ORDER BY id
''',
                              available=available)
        return [Product(*row) for row in rows]


    @staticmethod
    def get_all_by_seller(id, available=True):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE seller_id = :id
AND available = :available
ORDER BY id
''',
                              id=id,
                              available=available)
        
        return [Product(*row) for row in rows]
    
    @staticmethod
    def remove_listing(id):
        try: 
            app.db.execute('''
    UPDATE Products
    SET available=false
    WHERE id = :id
    RETURNING id
    ''',
                                id=id)
            print("Deleted: ", id)
            return id
        except Exception  as e:
            print(e)
            print("Could not delete: ", id)
            return None

    @staticmethod
    def change_quantity(id, quantity):
        try: 
            app.db.execute('''
    UPDATE Products
    SET quantity=:quantity
    WHERE id = :id
    RETURNING id
    ''',
                                id=id,
                                quantity=quantity)
            return id
        except Exception  as e:
            print(e)
            print("Could not change quantity: ", id)
            return None

    @staticmethod
    def change_price(id, price):
        try: 
            app.db.execute('''
    UPDATE Products
    SET price=:price
    WHERE id = :id
    RETURNING id
    ''',
                                id=id,
                                price=price)
            return id
        except Exception  as e:
            print(e)
            print("Could not change quantity: ", id)
            return None
    
    @staticmethod
    def editInfo(id, name, description, imageLink, category):
        try: 
            app.db.execute('''
    UPDATE Products
    SET name = :name, description = :description, imageLink = :imageLink, category = :category
    WHERE id = :id
    RETURNING id
    ''',
                                id=id,
                                  name=name,
                                  description=description,
                                  imageLink=imageLink,
                                  category=category)
            return id
        except Exception  as e:
            print(e)
            print("Could not change quantity: ", id)
            return None

    @staticmethod
    def change_description(id, description):
        try: 
            app.db.execute('''
    UPDATE Products
    SET description=:description
    WHERE id = :id
    RETURNING id
    ''',
                                id=id,
                                description=description)
            return id
        except Exception  as e:
            print(e)
            print("Could not change description: ", id)
            return None

    @staticmethod
    def decrease_purchased_quantity(purchased_items):
        try: 
            for item in purchased_items:
                id = item.product_id
                amount = item.quantity
                rows = app.db.execute('''
                    UPDATE Products
                    SET quantity= quantity - :amount
                    WHERE id = :id
                    ''',
                                id=id,
                                amount=amount)
            return id
        except Exception  as e:
            print(e)
            print("Decreasing purchased items failed")


    @staticmethod
    def new_listing(seller_id, name, quantity, description, imageLink, category, price):
        try:
            rows = app.db.execute("""
                INSERT INTO Products(id, seller_id, name, description, imageLink, category, price, available, quantity)
                VALUES(DEFAULT, :seller_id, :name, :description, :imageLink, :category, :price, TRUE, :quantity)
                returning id
                """,
                                  name=name,
                                  quantity=quantity,
                                  description=description,
                                  imageLink=imageLink,
                                  category=category,
                                  price=price,
                                  seller_id=seller_id)
            id = rows[0][0]
            print("Inserted: ", id)
            return Product.get(id)
        except Exception as e:
            print(e)
            # likely email already in use; better error checking and
            # reporting needed
            print("not added")
            return None

    @staticmethod
    def get_best_selling(available=True):
        rows = app.db.execute('''
SELECT id, name, products.price, imageLink, SUM(order_history.quantity) 
FROM (PRODUCTS left join order_history on products.id=order_history.product_id) 
WHERE available = :available
GROUP BY id 
ORDER BY sum DESC NULLS LAST LIMIT 7;
''',
                              available=available)
        
        return [row for row in rows]


    @staticmethod
    def get_top_rated(available=True):
        rows = app.db.execute('''
SELECT products.id, name, price, imageLink, avg(rating) 
FROM (products left join product_rating on products.id=product_rating.product_id) 
WHERE available = :available
group by products.id ORDER BY avg DESC NULLS LAST LIMIT 7;
''',
                              available=available)
        
        return [row for row in rows]






