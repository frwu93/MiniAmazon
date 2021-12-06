from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, product_name, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.product_name = product_name
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT Orders.order_id, buyer_id, Order_History.product_id, Products.name, time_ordered
FROM Orders, Order_History, Products
WHERE buyer_id = :uid
AND Orders.order_id = Order_History.order_id
AND Order_History.product_id = Products.id
AND time_ordered >= :since
ORDER BY time_ordered DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
