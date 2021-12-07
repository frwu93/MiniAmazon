from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request


class Coupon:
    def __init__(self, code, percent_off, product_id, product_name, price):
        self.code = code
        self.percent_off = percent_off
        self.product_id = product_id
        self.product_name = product_name
        if price is not None:
            self.amount_saved = '{:.2f}'.format(price*(1-percent_off/100))


    @staticmethod
    def find_coupon(code):
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
            print(e)
            print("Couldn't find coupon")

    @staticmethod
    def is_expired(code):
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
            print(len(rows))
            return len(rows) == 0
        except Exception as e:
            print(e)
            print("Couldn't find coupon")


    @staticmethod
    def new_coupon(code, percent, start, end, product_id):
        try:
            rows = app.db.execute("""
                INSERT INTO Coupons(coupon_code, percent_off, start_date, end_date)
                VALUES(:code, :percent, :start, :end)
                returning coupon_code
                """,
                                  code=code,
                                  percent=percent,
                                  start=start,
                                  end=end)
            coupon = rows[0][0]
            print("Inserted: ", coupon)

            rows = app.db.execute("""
                INSERT INTO Product_Coupons(coupon, product_id)
                VALUES(:code, :product_id)
                returning coupon
                """,
                                  code=code,
                                  product_id=product_id)

            flash("Coupon created: " + code + " for product " + str(product_id))
            return coupon
        except Exception as e:
            print(e)
            # likely email already in use; better error checking and
            # reporting needed
            print("not added")
            return None
    
    