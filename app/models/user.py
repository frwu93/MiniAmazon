from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from .. import login


class User(UserMixin):
    def __init__(self, password, id, email, firstname, lastname, address, balance, imageLink):
        """
        All the relevant information regarding the user
        Args:
            password (String): password of user
            id (integer): id of the user
            email (String): the email of the user
            firstname (String): the first name of the user
            lastname (String): the last name of the user
            address (String): the address of the user
            balance (Float): the balance of the user
            imageLink (String): the imagelink of the user
        """
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = '{:.2f}'.format(balance)
        self.password = password
        self.imageLink = imageLink

    @staticmethod
    def get_by_auth(email, password):
        """
        Gets all the information after authenticating user
        Args:
            email (String): the email of the user
            password (String): password of user
        
        Returns:
            User: returns the user object with correspoding information
        """

        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance, imageLink
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
        """
        Checks if the email already exists
        Args:
            email (String): the email of the user

        Returns:
            boolean: whether email exists or not
        """
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address):
        """
        Registers the user and updates the database accordingly
        Args:
            email (String): the email of the user
            firstname (String): the first name of the user
            lastname (String): the last name of the user
            address (String): the address of the user

        Returns:
            integer: id of the user
        """
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
        """
        Gets the information for the user with given id
        Args:
            id (integer): id of the user

        Returns:
            User: user object with all relevant information
        """
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance, imageLink
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def updateFirstName(id, newName):
        """
        Updates the firstname of the user
        Args:
            id (integer): id of the user
            newName (String): new first name of the user

        Returns:
            integer: id of the user
        """
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
        """
        Updates the lastname of the user
        Args:
            id (integer): id of the user
            newName (String): new last name of the user

        Returns:
            integer: id of the user
        """
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
        """
        Updates the email of the user
        Args:
            id (integer): id of the user
            newEmail (String): new email of the user

        Returns:
            integer: id of the user
        """
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
        """
        Updates the address of the user
        Args:
            id (integer): id of the user
            newAddress (String): new address of the user

        Returns:
            integer: id of the user
        """
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
        """
        Updates the password of the user
        Args:
            id (integer): id of the user
            newPassword (String): new password of the user

        Returns:
            integer: id of the user
        """
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
        """
        Updates the balance of the user from a deposit
        Args:
            id (integer): id of the user
            deposit (float): deposit amount

        Returns:
            integer: id of the user
        """
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
        """
        Updates the balance_history table from a deposit
        Args:
            user_id (integer): id of the user
            amount (float): amount of the deposit
            time_initiated (timestamp): time deposit was initiated
            cur_balance (float): running balance from deposit

        Returns:
            integer: id of the user
        """
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
        """
        Updates the balance of the user from a withdrawal
        Args:
            id (integer): id of the user
            withdrawal (float): withdrawal amount

        Returns:
            integer: id of the user
        """
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
        """
        Updates the balance_history table from a withdrawal
        Args:
            user_id (integer): id of the user
            amount (float): amount of the withdrawal
            time_initiated (timestamp): time withdrawal was initiated
            cur_balance (float): running balance from withdrawal

        Returns:
            integer: id of the user
        """
        try:
            rows = app.db.execute('''
            INSERT INTO Balance_History(uid, amount, balance_type, cur_balance, time_initiated)
            VALUES(:user_id, -1.0 * CAST(:amount AS FLOAT), 'W', :cur_balance, :time_initiated)
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
    def updateProfilePic(id, imageLink):
        """
        Updates the profilepic of the user
        Args:
            id (integer): id of the user
            imageLink (String): new image link of the user

        Returns:
            integer: id of the user
        """
        rows = app.db.execute("""
UPDATE Users
SET imageLink=:imageLink
WHERE id = :id
RETURNING id
""",
id=id,
imageLink=imageLink)
        return id

    @staticmethod
    def add_purchase(user_id, amount, time_initiated, cur_balance, product_name, quantity):
        """
        Updates the balance_history table from a purchase
        Args:
            user_id (integer): id of the user
            amount (float): amount of the purchase
            time_initiated (timestamp): time purchase was initiated
            cur_balance (float): running balance from purchase
            product_name (String): name of the product of the purchase
            quantity (integer): quantity of products bought

        Returns:
            integer: id of the user
        """
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

    @staticmethod
    def add_sold(user_id, amount, time_initiated, cur_balance, product_name, quantity):
        """
        Updates the balance_history table when user makes a sell
        Args:
            user_id (integer): id of the user
            amount (float): amount of the purchase
            time_initiated (timestamp): time purchase was initiated
            cur_balance (float): running balance from purchase
            product_name (String): name of the product of the purchase
            quantity (integer): quantity of products bought

        Returns:
            integer: id of the user
        """
        try:
            rows = app.db.execute('''
            INSERT INTO Balance_History(uid, amount, balance_type, cur_balance, time_initiated)
            VALUES(:user_id, :amount, CONCAT('Sold ', :product_name, ': x', CAST(:quantity AS varchar)), :cur_balance, :time_initiated)
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

    @staticmethod
    def isSeller(id):
        """
        Checks if user with given id is a seller or not
        Args:
            id (integer): id of the user

        Returns:
            boolean: whether user is a seller
        """
        try:
            rows = app.db.execute("""
                SELECT * FROM Sellers
                WHERE id=:id
                """,
                id=id)
            if len(rows) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def updateSellers(id):
        """
        Updates the seller table
        Args:
            id (integer): id of the new seller

        Returns:
            integer: id of the user
        """
        try:
            rows = app.db.execute('''
            INSERT INTO Sellers(id)
            VALUES(:id)
            RETURNING id
            ''',
                    id = id)
            return id
        except Exception as e:
            print(e)
            print("Seller Registration Failed")
