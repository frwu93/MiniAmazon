import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

Faker.seed(0)
fake = Faker()

sellers = pd.read_csv('data/sellers_large.csv')

def gen_datetime(min_year=2019, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

ratings = pd.DataFrame(columns = ['seller_id','buyer_id','rating','time_reviewed'])
for i in range(1,500):
    buyer_id = i
    for i in range(10):
        seller_id = sellers.iloc[[0,fake.random_int(min=0, max=len(sellers)-1)]]
        rating = random.randint(0,5)
        time = gen_datetime().strftime("%m-%d-%Y %H:%M:%S")
        new_row = {'seller_id':seller_id, 'buyer_id':buyer_id, 'rating':rating, 'time':time}
        ratings = ratings.append(new_row, ignore_index = True)

ratings.to_csv('data/seller_ratings_large.csv', header = False, index = False)