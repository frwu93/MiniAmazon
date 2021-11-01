import pandas as pd
import random
from datetime import datetime, timedelta

products = pd.read_csv('data/products_large.csv')
buyers = pd.read_csv('data/buyers_large.csv')

def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

orders = pd.DataFrame(columns = ['buyer_id','product_id','time','quantity'])
for i in range(1,500):
    buyer_id = i
    for i in range(3):
        product_id = random.randint(1,len(products))
        quantity = random.randint(1,3)
        time = gen_datetime().strftime("%m-%d-%Y %H:%M:%S")
        new_row = {'buyer_id':buyer_id, 'product_id': product_id, 'time':time, 'quantity':quantity}
        orders = orders.append(new_row, ignore_index = True)

orders.to_csv('data/order_history_large.csv', header = False, index = False)