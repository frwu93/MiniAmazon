from flask import current_app as app


class Public_User_Products:
    def __init__(self, product_id, product_name, price, quantity):
        self.id = product_id
        self.name = product_name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get_public_user_products_by_uid(id):
        rows = app.db.execute("""
            SELECT id, name, price, quantity
            FROM Products
            WHERE seller_id = :id
            ORDER BY name
            """,
                              id=id)
        return [Public_User_Products(*row) for row in rows]