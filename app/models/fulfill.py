from flask import current_app as app

class Fulfill:
    def __init__(self, id, product_id, buyer_id, buyer_address, time_ordered, price, quantity, fulfilled):
        self.id = id
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.buyer_address = buyer_address
        self.time_ordered = time_ordered
        self.price = price
        self.quantity = quantity
        if fulfilled:
            self.fulfilled = "Fulfilled"
        else:
            self.fulfilled = "Not Fulfilled"

    @staticmethod
    def get_all_by_uid_since(seller_id, since):
        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, address, time_ordered, price, quantity, fulfilled
FROM (SELECT order_id, buyer_id, time_ordered, product_id, o.price, o.quantity, fulfilled, seller_id
FROM (SELECT Orders.Order_id, buyer_id, time_ordered, product_id, price, quantity, fulfilled 
FROM Orders 
LEFT JOIN Order_History ON Orders.order_id = Order_History.order_id) AS o 
LEFT JOIN Products ON o.product_id = Products.id) as k LEFT JOIN Users ON k.buyer_id = Users.id
WHERE seller_id = :seller_id
AND time_ordered >= :since
ORDER BY time_ordered DESC, order_id
''',
                              seller_id=seller_id,
                              since=since)
        return [Fulfill(*row) for row in rows]
    
    @staticmethod
    def fulfill(order_id, product_id):
        try: 
            app.db.execute('''
    UPDATE Order_History
    SET fulfilled=TRUE
    WHERE order_id = :order_id
    AND product_id = :product_id
    RETURNING order_id, product_id
    ''',
                        order_id=order_id,
                        product_id=product_id)
        except Exception as e:
            print(e)
            print(f"Could not fulfill product: {product_id} for order: {order_id}")
            return None


        
