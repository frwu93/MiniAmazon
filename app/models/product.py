from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_by_seller(id, available=True):
        rows = app.db.execute('''
SELECT product_id, name, price, available
FROM Products, Sells
WHERE seller_id = :id
AND Products.id = Sells.product_id
AND available = :available
ORDER BY product_id
''',
                              id=id,
                              available=available)
        
        return [Product(*row) for row in rows]
    
    @staticmethod
    def remove_listing(id):
        try: 
            app.db.execute('''
    UPDATE Products
    SET available=false
    WHERE id = :id
    RETURNING id
    ''',
                                id=id)
            return id
        except Exception  as e:
            print(e)
            print("Could not delete: ", id)
            return None



    @staticmethod
    def new_listing(seller_id, name, quantity, description, imageLink, category, price):
        try:
            rows = app.db.execute("""
                INSERT INTO Products(id, name, description, imageLink, category, price, available)
                VALUES(DEFAULT, :name, :description, :imageLink, :category, :price, TRUE)
                returning id
                """,
                                  name=name,
                                  quantity=quantity,
                                  description=description,
                                  imageLink=imageLink,
                                  category=category,
                                  price=price)
            id = rows[0][0]
            rows2 = app.db.execute("""
                INSERT INTO Sells(seller_id, product_id, quantity)
                VALUES(:seller_id, :product_id, :quantity)
            """,
                            seller_id = seller_id,
                            product_id = id,
                            quantity = quantity)
            print("backend reg; inserted into db")
            return Product.get(id)
        except Exception as e:
            print(e)
            # likely email already in use; better error checking and
            # reporting needed
            print("not added")
            return None

