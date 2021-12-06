from flask import current_app as app


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
    
    