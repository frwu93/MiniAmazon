from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from .. import login


class User(UserMixin):
    def __init__(self, password, id, email, firstname, lastname, address, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = '{:.2f}'.format(balance)
        self.password = password

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][0:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
                INSERT INTO Users(id,email, password, firstname, lastname, address,balance)
                VALUES(DEFAULT, :email, :password, :firstname, :lastname, :address, 0.0)
                RETURNING id
                """,
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname,
                                  address = address)
            id = rows[0][0]
            print("backend reg; inserted into db")
            rows3 = app.db.execute("""
                INSERT INTO Sellers(id)
                VALUES(:id)
                RETURNING id
                """,
                id = id)
            print("added to sellers")
            return User.get(id)
        except Exception as e:
            print(e)
            # likely email already in use; better error checking and
            # reporting needed
            print("not added")
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def updateFirstName(id, newName):
        rows = app.db.execute("""
UPDATE Users
SET firstname=:newName
WHERE id = :id
RETURNING id
""",
id=id,
newName=newName)
        return id

    @staticmethod
    def updateLastName(id, newName):
        rows = app.db.execute("""
UPDATE Users
SET lastname=:newName
WHERE id = :id
RETURNING id
""",
id=id,
newName=newName)
        return id

    @staticmethod
    def updateEmail(id, newEmail):
        try:
            rows = app.db.execute("""
                UPDATE Users
                SET email=:newEmail
                WHERE id = :id
                RETURNING id
                """,
                id=id,
                newEmail=newEmail)
            return id
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def updateAddress(id, newAddress):
        try:
            rows = app.db.execute("""
                UPDATE Users
                SET address=:newAddress
                WHERE id = :id
                RETURNING id
                """,
                id=id,
                newAddress=newAddress)
            return id
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def updatePassword(id, newPassword):
        newPassword = generate_password_hash(newPassword)
        try:
            rows = app.db.execute("""
                UPDATE Users
                SET password=:newPassword
                WHERE id = :id
                RETURNING id
                """,
                id=id,
                newPassword=newPassword)
            return id
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def updateBalanceDeposit(id, deposit):
        try:
            rows = app.db.execute("""
                UPDATE Users
                SET balance=balance + ROUND(:deposit,2)
                WHERE id = :id
                RETURNING id
                """,
                id=id,
                deposit=deposit)
            return id
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add_deposit(user_id, amount, time_initiated, cur_balance):
        try:
            rows = app.db.execute('''
            INSERT INTO Balance_History(uid, amount, balance_type, cur_balance, time_initiated)
            VALUES(:user_id, :amount, 'D', :cur_balance, :time_initiated)
            RETURNING uid
            ''',
                    user_id = user_id,
                    amount = amount,
                    time_initiated = time_initiated,
                    cur_balance = cur_balance)
            user_id = rows[0][0]
            return user_id
        except Exception as e:
            print(e)
            print("Deposit Failed")

    @staticmethod
    def updateBalanceWithdrawal(id, withdrawal):
        try:
            rows = app.db.execute("""
                UPDATE Users
                SET balance=balance - ROUND(:withdrawal,2)
                WHERE id = :id
                RETURNING id
                """,
                id=id,
                withdrawal=withdrawal)
            return id
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add_withdrawal(user_id, amount, time_initiated, cur_balance):
        try:
            rows = app.db.execute('''
            INSERT INTO Balance_History(uid, amount, balance_type, cur_balance, time_initiated)
            VALUES(:user_id, -1 * :amount, 'W', :cur_balance, :time_initiated)
            RETURNING uid
            ''',
                    user_id = user_id,
                    amount = amount,
                    time_initiated = time_initiated,
                    cur_balance = cur_balance)
            user_id = rows[0][0]
            return user_id
        except Exception as e:
            print(e)
            print("Withdrawal Failed")

    @staticmethod
    def add_purchase(user_id, amount, time_initiated, cur_balance, product_name, quantity):
        try:
            rows = app.db.execute('''
            INSERT INTO Balance_History(uid, amount, balance_type, cur_balance, time_initiated)
            VALUES(:user_id, :amount, CONCAT('Purchased ', :product_name, ': x', CAST(:quantity AS varchar)), :cur_balance, :time_initiated)
            RETURNING uid
            ''',
                    user_id = user_id,
                    amount = amount,
                    time_initiated = time_initiated,
                    cur_balance = cur_balance,
                    product_name = product_name,
                    quantity = quantity)
            user_id = rows[0][0]
            return user_id
        except Exception as e:
            print(e)
            print("Purchase Failed")

