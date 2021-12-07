from flask import current_app as app


class Balance_History:
    def __init__(self, amount, time_initiated, balance_type, balance):
        """
        All the information relevant for the balance_history page
        Args:
            amount (float): amount of transaction
            time_initiated (timestamp): the time when transaction was made
            balance_type (String): type of the transaction
            balance (float): the running balance after transaction
        """
        self.date = time_initiated
        if balance_type == "D" or balance_type == "W":
            if amount < 0:
                self.description = "Withdrawal of $" + str('{:.2f}'.format(-1 * amount))
                self.amount = "- $" + str('{:.2f}'.format(-1 * amount))
            else:
                self.description = "Deposit of $" + str('{:.2f}'.format(amount))
                self.amount = "+ $" + str('{:.2f}'.format(amount))
        else:
            self.description = balance_type
            if balance_type[0:4] == "Sold":
                self.amount = "+ $" + str('{:.2f}'.format(amount))
            else:
                self.amount = "- $" + str('{:.2f}'.format(amount))
        self.current_balance = "$" + str('{:.2f}'.format(balance))

    @staticmethod
    def get_balance_history_by_uid(id):
        """
        Gets the information for the balance history for the user with given id
        Args:
            id (integer): id of the user

        Returns:
            Balance_History: Balance history object with all relevant information
        """
        rows = app.db.execute("""
            SELECT amount, time_initiated, balance_type, cur_balance
            FROM Balance_History
            WHERE uid = :id
            ORDER BY time_initiated DESC
            """,
                              id=id)
        return [Balance_History(*row) for row in rows]

        