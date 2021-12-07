import pandas as pd
import random
from faker import Faker
from datetime import datetime

Faker.seed(0)
fake = Faker()

coupons = pd.DataFrame(columns = ['coupon_code','percent_off','start_date','end_date'])

for i in range(1000):
    coupon_code = fake.pystr(min_chars = 3, max_chars = 10).upper()
    percent_off = fake.random_int(min = 1, max = 100)
    start_date = fake.date_time_this_decade()
    end_date = fake.date_time_between_dates(datetime_start = start_date, datetime_end = datetime(2023, 1, 1, 00, 00, 00))
    start_date = start_date.strftime("%m-%d-%Y %H:%M:%S")
    end_date = end_date.strftime("%m-%d-%Y %H:%M:%S")
    new_row = {'coupon_code': coupon_code, 'percent_off':percent_off, 'start_date':start_date, 'end_date':end_date}
    coupons = coupons.append(new_row, ignore_index = True)
coupons = coupons.drop_duplicates(subset = ['coupon_code'])
coupons.to_csv('./data/Coupons_large.csv', header = False, index = False)