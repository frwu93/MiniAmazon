import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

Faker.seed(0)
fake = Faker()

def gen_datetime(min_year=2019, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

    
order_hist = pd.read_csv('./data/Order_History_large.csv', header = None)
coupons = pd.read_csv('./data/Coupons_large.csv', header = None)
orders = pd.DataFrame(columns = ['buyer_id','total_cost', 'time_ordered', 'coupon_used'])

order_ids = range(1,10001)

for i in order_ids:
    print(i)
    buyer_id = fake.random_int(min=1, max = 1000)
    total_cost = '{:.2f}'.format(order_hist.loc[order_hist.iloc[:,0] == i].iloc[:,2].sum())
    time_ordered = gen_datetime().strftime("%m-%d-%Y %H:%M:%S")
    usedCoupon = fake.boolean(chance_of_getting_true = 50)
    if (usedCoupon):
        coupon = coupons.iloc[fake.random_int(min = 0, max = len(coupons)-1), 0]
    else:
        coupon = None
    new_row = {'buyer_id':buyer_id, 'total_cost':total_cost, 'time_ordered':time_ordered, 'coupon_used':coupon}
    orders = orders.append(new_row, ignore_index = True)

orders.to_csv('./data/Orders_large.csv', header = False, index = False)