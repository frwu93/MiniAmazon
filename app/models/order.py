from flask import current_app as app

class Order:
    def __init__(self, id, buyer_id, time_ordered, coupon):
        self.id = id
        self.buyer_id = buyer_id
        self.time_ordered = time_ordered
        self.coupon = coupon

    @staticmethod
    def add_order(buyer_id, total_cost, coupon):
        try:
            rows = app.db.execute('''
            INSERT INTO Orders(buyer_id, total_cost, coupon_used)
            VALUES(:buyer_id, :total_cost, :coupon)
            RETURNING order_id
            ''',
                    buyer_id = buyer_id,
                    total_cost = total_cost,
                    coupon = coupon)
            order_id = rows[0][0]
            return order_id
        except Exception as e:
            print(e)
            print("Adding to Orders Failed")
    
    @staticmethod
    def add_to_history(id, purchased_items):
        try:
            for item in purchased_items:
                print("INSERTION IS HAPPENING")
                product = item.product_id
                price = item.price
                quantity = item.quantity
                rows = app.db.execute('''
                INSERT INTO Order_History(order_id, product_id, price, quantity)
                VALUES(:id, :product, :price, :quantity)
                RETURNING product_id
                ''',
                        id = id,
                        product = product,
                        price = price,
                        quantity = quantity)
        except Exception as e:
            print(e)
            print("Adding to Order History Failed - HISTORY HAS BEEN LOST")
    
    @staticmethod
    def get_coupon(id):
        try:
            rows = app.db.execute('''
            SELECT coupon_used
            FROM Orders
            WHERE order_id = :id
            ''',
                    id = id)
            coupon_used = rows[0][0]
            return coupon_used
        except Exception as e:
            print(e)
            print("Couldn't find used coupon")
    
