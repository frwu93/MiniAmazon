from flask import current_app as app


class Purchase_History:
    def __init__(self, order_id, time_ordered, product_name, price, quantity, fulfillment_status):
        self.order_id = order_id
        self.time_ordered = time_ordered
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.fulfillment_status = fulfillment_status
        self.order_cost = '{:.2f}'.format(price*quantity)
        self.order_link = "<Link>"

    @staticmethod
    def get_purchase_history_by_uid(id):
        rows = app.db.execute("""
            SELECT Order_History.order_id, Orders.time_ordered, Products.name, Order_History.price, Order_History.quantity, Order_History.fulfilled
            FROM Order_History, Orders, Products
            WHERE Orders.buyer_id = :id AND Order_History.order_id = Orders.order_id AND Order_History.product_id = Products.id
            ORDER BY Orders.time_ordered DESC
            """,
                              id=id)
        return [Purchase_History(*row) for row in rows]