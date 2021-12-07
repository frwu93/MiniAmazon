from flask import current_app as app


class Cart:
    def __init__(self, product_id, product_name, seller_id, firstname, lastname, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.seller_id = seller_id
        self.seller = firstname + " " + lastname
        self.price = price
        self.quantity = quantity
        self.order_cost = '{:.2f}'.format(price*quantity)

    @staticmethod
    def get_cart_products_by_uid(buyer_id):
        rows = app.db.execute('''
        SELECT Products.id, Products.name, Products.seller_id, Users.firstname, Users.lastname, price, Cart.quantity
        FROM Cart, Products, Users
        WHERE Cart.buyer_id = :buyer_id AND Cart.product_id = Products.id AND 
        Users.id = seller_id AND
        Cart.saved = FALSE
        ''',
                              buyer_id=buyer_id)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_saved_products_by_uid(buyer_id):
        rows = app.db.execute('''
        SELECT Products.id, Products.name, Products.seller_id, Users.firstname, Users.lastname, price, Cart.quantity
        FROM Cart, Products, Users
        WHERE Cart.buyer_id = :buyer_id AND Cart.product_id = Products.id AND 
        Users.id = seller_id AND
        Cart.saved = TRUE
        ''',
                              buyer_id=buyer_id)
        return [Cart(*row) for row in rows]


    
    @staticmethod
    def get_subtotal(cart : list) -> float:
        total = 0
        for product in cart:
            total += float(product.order_cost)
        return total
    
    @staticmethod
    def change_quantity(buyer_id, product_id, quantity):
        try: 
            app.db.execute('''
    UPDATE Cart
    SET quantity=:quantity
    WHERE buyer_id = :buyer_id AND product_id = :product_id
    RETURNING product_id
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
            RETURNING product_id
            ''', 
                                buyer_id = buyer_id, 
                                product_id = product_id)
        except Exception as e:
            print(e)
            print(f'Could note delete {product_id}')
            return None
    
    @staticmethod
    def add_to_cart(buyer_id, product_id, quantity):
        try:
            rows = app.db.execute('''
            INSERT INTO Cart(buyer_id, product_id, quantity, saved)
            VALUES(:buyer_id, :product_id, :quantity, FALSE)
            RETURNING buyer_id, product_id
            ''',
                    buyer_id = buyer_id,
                    product_id = product_id,
                    quantity = quantity)
            buyer_id = rows[0][0]
            return buyer_id
        except Exception as e:
            print(e)
            print("Adding to Cart Failed")
            return None

    @staticmethod
    def add_to_saved(buyer_id, product_id):
        try:
            rows = app.db.execute('''
            INSERT INTO Cart(buyer_id, product_id, quantity, saved)
            VALUES(:buyer_id, :product_id, :quantity, TRUE)
            RETURNING buyer_id, product_id
            ''',
                    buyer_id = buyer_id,
                    product_id = product_id,
                    quantity = 1)
            buyer_id = rows[0][0]
            return buyer_id
        except Exception as e:
            print(e)
            print("Adding to Saved Failed")
            return None
    
    @staticmethod
    def clear_user_cart(buyer_id):
        try:
            rows = app.db.execute('''
            DELETE FROM Cart
            WHERE buyer_id = :buyer_id
            AND saved = FALSE
            ''',
                    buyer_id = buyer_id)
        except Exception as e:
            print(e)
            print("Clearing Cart failed")

    @staticmethod
    def toggle_saved(buyer_id, product_id):
        try:
            rows = app.db.execute('''
            UPDATE Cart
            SET saved = 
                CASE WHEN 
                    saved = TRUE THEN FALSE
                    ELSE TRUE 
                END
            WHERE buyer_id = :buyer_id AND product_id = :product_id
            ''',
                    buyer_id = buyer_id,
                    product_id = product_id)
        except Exception as e:
            print(e)
            print("Toggling saved failed")
    
    @staticmethod
    def contains_item(buyer_id, product_id):
        try:
            rows = app.db.execute('''
            SELECT 
            FROM Cart
            WHERE buyer_id = :buyer_id 
            AND product_id = :product_id
            AND saved = FALSE
            ''',
                    buyer_id = buyer_id,
                    product_id = product_id)
            return len(rows) > 0
        except Exception as e:
            print(e)
            print("can't find item")

    