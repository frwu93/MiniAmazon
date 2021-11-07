from flask import current_app as app


class Cart:
    def __init__(self, product_id, product_name, firstname, lastname, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.seller = firstname + " " + lastname
        self.price = price
        self.quantity = quantity
        self.total_cost = '{:.2f}'.format(price*quantity)

    @staticmethod
    def get_cart_products_by_uid(buyer_id):
        rows = app.db.execute('''
        SELECT Products.id, Products.name, Users.firstname, Users.lastname, price, Cart.quantity
        FROM Cart, Products, Users
        WHERE Cart.buyer_id = :buyer_id AND Cart.product_id = Products.id AND 
        Users.id = seller_id
        ''',
                              buyer_id=buyer_id)
        return [Cart(*row) for row in rows]


    
    @staticmethod
    def get_subtotal(cart : list) -> float:
        total = 0
        for product in cart:
            total += float(product.total_cost)
        return '{:.2f}'.format(total)
    
    @staticmethod
    def change_quantity(buyer_id, product_id, quantity):
        try: 
            app.db.execute('''
    UPDATE Cart
    SET quantity=:quantity
    WHERE buyer_id = :buyer_id AND product_id = :product_id
    ''',
                                buyer_id=buyer_id,
                                product_id = product_id,
                                quantity=quantity)
        except Exception as e:
            print(e)
            print(f"Could not change quantity of {product_id} to {quantity}")
            return None

    @staticmethod
    def delete_item(buyer_id, product_id):
        try:
            app.db.execute('''
            DELETE FROM Cart
            WHERE buyer_id = :buyer_id AND product_id = :product_id
            ''', 
                                buyer_id = buyer_id, 
                                product_id = product_id)
        except Exception as e:
            print(e)
            print(f'Could note delete {product_id}')
            return None
    