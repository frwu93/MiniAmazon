from flask import current_app as app


class Cart:
    def __init__(self, product_id, product_name, seller_id, firstname, lastname, price, quantity):
        """
        Creates a cart item object

        Args:
            product_id (int): product ID of item 
            product_name (str): name of item
            seller_id (int): user ID of item's seller
            firstname (str): first name of item's seller
            lastname (str): last name of item's seller
            price (float): price of item
            quantity (int): amount of item
        """
        self.product_id = product_id
        self.product_name = product_name
        self.seller_id = seller_id
        self.seller = firstname + " " + lastname
        self.price = price
        self.quantity = quantity
        self.order_cost = '{:.2f}'.format(price*quantity)

    @staticmethod
    def get_cart_products_by_uid(buyer_id):
        """
        Gets all items in a given user's cart

        Args:
            buyer_id (int): User ID of the desired cart

        Returns:
            (list) : list of items in the cart
        """
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
        """
        Gets all items in a given user's saved for later list

        Args:
            buyer_id (int): User ID of the desired saved for later list

        Returns:
            (list): items in saved for later list
        """
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
    def change_quantity(buyer_id, product_id, quantity):
        """
        Changes the quantity of an item in the cart, modifies Cart table

        Args:
            buyer_id (int): user ID of that cart's user
            product_id (int): product ID of product being modified
            quantity (int): new quantity
        """
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
            return None

    @staticmethod
    def delete_item(buyer_id, product_id):
        """
        Deletes an item from the user's cart or saved for later list.
        Deletion in Cart table

        Args:
            buyer_id (int): user ID of cart's user
            product_id (int): product ID of product being deleted

        Returns:
            (int): Product ID of deleted product
        """
        try:
            app.db.execute('''
            DELETE FROM Cart
            WHERE buyer_id = :buyer_id AND product_id = :product_id
            RETURNING product_id
            ''', 
                                buyer_id = buyer_id, 
                                product_id = product_id)
        except Exception as e:
            print(f'Could note delete {product_id}')
            return None
    
    @staticmethod
    def add_to_cart(buyer_id, product_id, quantity):
        """
        Adds an item to the user's cart in the Cart table

        Args:
            buyer_id (int): user ID of that cart's user
            product_id (int): product ID of product being added to cart
            quantity (int): quantity being added

        Returns:
            (int): product ID of product added
        """
        try:
            rows = app.db.execute('''
            INSERT INTO Cart(buyer_id, product_id, quantity, saved)
            VALUES(:buyer_id, :product_id, :quantity, FALSE)
            RETURNING buyer_id, product_id
            ''',
                    buyer_id = buyer_id,
                    product_id = product_id,
                    quantity = quantity)
            product_id = rows[0][1]
            return product_id
        except Exception as e:
            print("Adding to Cart Failed")
            return None

    @staticmethod
    def add_to_saved(buyer_id, product_id):
        """
        Adds an item to the user's cart in the Cart table


        Args:
           buyer_id (int): user ID of that cart's user
            product_id (int): product ID of product being added to saved for later list

        Returns:
            (int): product ID of product added
        """
        try:
            rows = app.db.execute('''
            INSERT INTO Cart(buyer_id, product_id, quantity, saved)
            VALUES(:buyer_id, :product_id, :quantity, TRUE)
            RETURNING buyer_id, product_id
            ''',
                    buyer_id = buyer_id,
                    product_id = product_id,
                    quantity = 1)
            product_id = rows[0][1]
            return product_id
        except Exception as e:
            print("Adding to Saved Failed")
            return None
    
    @staticmethod
    def clear_user_cart(buyer_id):
        """
        Clears a user's cart in the Cart table.
        Saved for later list still preserved

        Args:
            buyer_id (int): user ID of cart's user
        """
        try:
            rows = app.db.execute('''
            DELETE FROM Cart
            WHERE buyer_id = :buyer_id
            AND saved = FALSE
            ''',
                    buyer_id = buyer_id)
        except Exception as e:
            print("Clearing Cart failed")

    @staticmethod
    def toggle_saved(buyer_id, product_id):
        """
        If product is in cart, it moves it to saved for later.
        If product is in saved for later, it moves it to cart

        Args:
             buyer_id (int): user ID of that cart's user
            product_id (int): product ID of product being changed
        """
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
            print("Toggling saved failed")
    
    @staticmethod
    def contains_item(buyer_id, product_id):
        """Checks that an item is in the buyer's cart

        Args:
            buyer_id (int): user ID of that cart's user
            product_id (int): product ID of product being checked

        Returns:
            (boolean): true if product is in cart, false otherwise
        """
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
            print("can't find item")

    