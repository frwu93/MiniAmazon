from flask import current_app as app


class Product:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, quantity
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, quantity
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]


    @staticmethod
    def get_all_by_seller(id, available=True):
        rows = app.db.execute('''
SELECT id, name, price, quantity
FROM Products
WHERE seller_id = :id
AND available = :available
ORDER BY id
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
            print("Deleted: ", id)
            return id
        except Exception  as e:
            print(e)
            print("Could not delete: ", id)
            return None

    @staticmethod
    def change_quantity(id, quantity):
        try: 
            app.db.execute('''
    UPDATE Products
    SET quantity=:quantity
    WHERE id = :id
    RETURNING id
    ''',
                                id=id,
                                quantity=quantity)
            return id
        except Exception  as e:
            print(e)
            print("Could not change quantity: ", id)
            return None


    @staticmethod
    def new_listing(seller_id, name, quantity, description, imageLink, category, price):
        try:
            rows = app.db.execute("""
                INSERT INTO Products(id, seller_id, name, description, imageLink, category, price, available, quantity)
                VALUES(DEFAULT, :seller_id, :name, :description, :imageLink, :category, :price, TRUE, :quantity)
                returning id
                """,
                                  name=name,
                                  quantity=quantity,
                                  description=description,
                                  imageLink=imageLink,
                                  category=category,
                                  price=price,
                                  seller_id=seller_id)
            id = rows[0][0]
            print("Inserted: ", id)
            return Product.get(id)
        except Exception as e:
            print(e)
            # likely email already in use; better error checking and
            # reporting needed
            print("not added")
            return None


