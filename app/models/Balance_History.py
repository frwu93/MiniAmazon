from flask import current_app as app


class Balance_History:
    def __init__(self, amount, time_initiated, balance_type, balance):
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
            self.amount = "- $" + str('{:.2f}'.format(amount))
        self.current_balance = "$" + str('{:.2f}'.format(balance))

    @staticmethod
    def get_balance_history_by_uid(id):
        rows = app.db.execute("""
            SELECT amount, time_initiated, balance_type, cur_balance
            FROM Balance_History
            WHERE uid = :id
            ORDER BY time_initiated DESC
            """,
                              id=id)
        return [Balance_History(*row) for row in rows]

        