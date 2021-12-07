from flask import current_app as app


class Public_User_Products:
    def __init__(self, product_id, product_name, price, quantity):
        """
        Relevant infomation for the public users product page
        Args:
            product_id (integer): id of the product
            product_name (String): name of the product
            price (float): price of the product
            quantity (integer): quantity of the product
        """
        self.id = product_id
        self.name = product_name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get_public_user_products_by_uid(id):
        """
        Gets the all the product information for the current seller given id
        Args:
            id (integer): id of the seller

        Returns:
            Public_User_Products: Public user products object with all relevant information
        """
        rows = app.db.execute("""
            SELECT id, name, price, quantity
            FROM Products
            WHERE seller_id = :id
            ORDER BY name
            """,
                              id=id)
        return [Public_User_Products(*row) for row in rows]