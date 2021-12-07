import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

Faker.seed(0)
fake = Faker()

products = pd.read_csv('./data/Products_large.csv')
users = pd.read_csv('./data/Users_large.csv')

def gen_datetime(min_year=2019, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

ratings = pd.DataFrame(columns = ['buyer_id','product_id','rating','time_reviewed','description'])
for i in range(1,len(users)-1):
    buyer_id = i
    print(i)
    for i in range(5):
        product_id = fake.random_int(min=1, max=len(products)-1)
        rating = random.randint(0,5)
        time_reviewed = gen_datetime().strftime("%m-%d-%Y %H:%M:%S")
        description = fake.paragraph(nb_sentences=3)
        new_row = {'buyer_id':buyer_id,'product_id':product_id, 'rating':rating, 'time_reviewed':time_reviewed, 'description':description}
        ratings = ratings.append(new_row, ignore_index = True)
ratings = ratings.drop_duplicates(subset = ['product_id', 'buyer_id'])
ratings.to_csv('./data/Product_Rating_large.csv', header = False, index = False)