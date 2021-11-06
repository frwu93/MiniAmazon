from flask import current_app as app


class Cart:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    @staticmethod
    def get_all_by_uid(buyer_id):
        rows = app.db.execute('''
SELECT product_id, quantity
FROM Cart
WHERE buyer_id = :buyer_id
''',
                              buyer_id=buyer_id)
        return [Cart(*row) for row in rows]
    