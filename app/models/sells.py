from flask import current_app as app


class Sells:
    def __init__(self, seller_id, product_id, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.available = available


    #Find a product's seller by seller_id
    @staticmethod
    def get_by_pid(product_id):
        rows = app.db.execute('''
SELECT seller_id, product_id, quantity
FROM Sells
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Sells(*(rows[0])) if rows is not None else None
