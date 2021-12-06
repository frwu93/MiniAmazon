import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

Faker.seed(0)
fake = Faker()

sellers = pd.read_csv('./data/Sellers_large.csv')
users = pd.read_csv('./data/Users_large.csv')

def gen_datetime(min_year=2019, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

ratings = pd.DataFrame(columns = ['seller_id','buyer_id','rating','description','time_reviewed'])
for i in range(1,len(users)-1):
    print(i)
    buyer_id = i
    for i in range(10):
        seller_id = sellers.iloc[fake.random_int(min=0, max=len(sellers)-1),0]
        rating = random.randint(0,5)
        description = fake.paragraph(nb_sentences=3)
        time = gen_datetime().strftime("%m-%d-%Y %H:%M:%S")
        new_row = {'seller_id':seller_id, 'buyer_id':buyer_id, 'rating':rating, 'description': description, 'time_reviewed':time}
        ratings = ratings.append(new_row, ignore_index = True)
ratings = ratings.drop_duplicates(subset = ['seller_id', 'buyer_id'])
ratings.to_csv('./data/Seller_Rating_large.csv', header = False, index = False)