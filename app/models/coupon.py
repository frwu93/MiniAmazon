from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request


class Coupon:
    def __init__(self, code, percent_off, product_id, product_name, price):
        """
        Coupon object

        Args:
            code (str): coupon code
            percent_off (int): The percent off, stored as a number between 1-100, inclusive
            product_id (int): product ID of product, if the coupon is item-specific
            product_name (str): name of product if the coupon is item-specific
            price (str): String of new discounted price of item, if the coupon is item-specific
        """
        self.code = code
        self.percent_off = percent_off
        self.product_id = product_id
        self.product_name = product_name
        if price is not None:
            self.amount_saved = '{:.2f}'.format(price*(1-percent_off/100))


    @staticmethod
    def find_coupon(code):
        """
        Gets a coupon given the code

        Args:
            code (str): coupon code

        Returns:
            Coupon: coupon corresponding to the coupon code
        """
        try:
            rows = app.db.execute('''
            SELECT coupon_code, percent_off, product_id, name, price
            FROM COUPONS
            LEFT OUTER JOIN 
                (SELECT * FROM PRODUCT_COUPONS, PRODUCTS 
                WHERE coupon = :code AND product_id = id) AS PC
            ON COUPONS.coupon_code = coupon
            WHERE coupon_code = :code
            ''',
                    code = code)
            return Coupon(*(rows[0])) if rows is not None else None
        except Exception as e:
            print("Couldn't find coupon")

    @staticmethod
    def is_expired(code):
        """
        Checks that a coupon is not expired

        Args:
            code (str): coupon code

        Returns:
            (boolean): returns true if coupon is expired, false otherwise
        """
        try:
            rows = app.db.execute('''
            SELECT coupon_code, percent_off, product_id
            FROM COUPONS
            LEFT OUTER JOIN (SELECT * FROM PRODUCT_COUPONS WHERE coupon = :code) AS PC
            ON coupon_code = coupon
            WHERE COUPONS.coupon_code = :code
            AND current_timestamp >= start_date
            AND current_timestamp <= end_date
            ''',
                    code = code)
            return len(rows) == 0
        except Exception as e:
            print("Couldn't find coupon")


    @staticmethod
    def new_coupon(code, percent, start, end, product_id):
        """
        Adds a new coupon for a given item

        Args:
            code (str): coupon code of new coupon
            percent (int): percent discount given by new coupon
            start (str): start date of coupon
            end (str): end date of coupon
            product_id (int): product ID of coupon

        Returns:
            (str): the coupon code
        """
        
        try:
            rows = app.db.execute('''
                INSERT INTO Coupons(coupon_code, percent_off, start_date, end_date)
                VALUES(:code, :percent, :start, :end)
                returning coupon_code
                ''',
                                  code=code,
                                  percent=percent,
                                  start=start,
                                  end=end)
            coupon = rows[0][0]

            rows = app.db.execute('''
                INSERT INTO Product_Coupons(coupon, product_id)
                VALUES(:code, :product_id)
                returning coupon
                ''',
                                  code=code,
                                  product_id=product_id)

            flash("Coupon created: " + code + " for product " + str(product_id))
            return coupon
        except Exception as e:
            # likely email already in use; better error checking and
            # reporting needed
            print("Coupon not added")
            return None
    
    