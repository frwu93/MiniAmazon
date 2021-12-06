from flask import current_app as app
from flask import Flask
from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


class Product:
    def __init__(self, id, seller_id, name, description, imageLink, category, price, available, quantity):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.description = description
        self.imageLink = imageLink
        self.category = category
        self.price = '{:.2f}'.format(price)
        self.available = available
        self.quantity = quantity

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







