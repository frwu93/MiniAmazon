from flask import current_app as app


class Purchase_History:
    def __init__(self, order_id, time_ordered, product_name, product_id, seller_id, firstname, lastname, price, quantity, fulfillment_status):
        self.order_id = order_id
        self.time_ordered = time_ordered
        self.product_name = product_name
        self.product_id = product_id
        self.seller_id = seller_id
        self.seller = firstname + " " + lastname
        self.price = price
        self.quantity = quantity
        self.fulfillment_status = fulfillment_status
        self.order_cost = '{:.2f}'.format(price*quantity)
        self.order_link = "<Link>"

    @staticmethod
    def get_purchase_history_by_uid(id):
        rows = app.db.execute("""
            SELECT Order_History.order_id, Orders.time_ordered, Products.name, product_id, Products.seller_id, Users.firstname, Users.lastname, Order_History.price, Order_History.quantity, Order_History.fulfilled
            FROM Order_History, Orders, Products, Users
            WHERE Orders.buyer_id = :id 
            AND Order_History.order_id = Orders.order_id 
            AND Order_History.product_id = Products.id
            AND Users.id = seller_id
            ORDER BY Orders.time_ordered DESC
            """,
                              id=id)
        return [Purchase_History(*row) for row in rows]
    

    @staticmethod
    def get_all_Sellers(id):
        rows = app.db.execute("""
            SELECT DISTINCT(Products.seller_id)
            FROM Order_History, Orders, Products
            WHERE Orders.buyer_id = :id AND Order_History.order_id = Orders.order_id AND Order_History.product_id = Products.id
            """,
                              id=id)
        if rows is not None:
            return [row[0] for row in rows]

