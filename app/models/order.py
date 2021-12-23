from flask import current_app as app

class Order:
    def __init__(self, id, buyer_id, time_ordered, coupon):
        """
        Creates an order object

        Args:
            id (int): order ID
            buyer_id (int): user ID of buyer
            time_ordered (str): timestamp of order placed
            coupon (str): coupon code that aas applied to the order, if applicable
        """
        self.id = id
        self.buyer_id = buyer_id
        self.time_ordered = time_ordered
        self.coupon = coupon

    @staticmethod
    def add_order(buyer_id, total_cost, coupon):
        """
        Adds a new order to the Orders table in the database

        Args:
            buyer_id (int): User ID of buyer
            total_cost (int): Total cost of the transaction
            coupon (str): Coupon used, if applicable. Null if no coupon used

        Returns:
            order_id (int) : order_id of new order inserted
        """
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
            print("Adding to Orders Failed")
    
    @staticmethod
    def add_to_history(id, purchased_items):
        """
        Adds items from a new order into the Order_History table,
        recording each item's price, quantity

        Args:
            id (int): order_id of the order
            purchased_items (list): List of items in that order
        """
        try:
            for item in purchased_items:
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
            print("Adding to Order History Failed")
    
    @staticmethod
    def get_coupon(id):
        """
        Returns coupon used by order given order ID. If no coupon is used,
        null is returned

        Args:
            id (int): Order ID

        Returns:
            (str): coupon code of coupon used
        """
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
            print("Couldn't find used coupon")
    
