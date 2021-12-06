import pandas as pd
import random
from datetime import datetime, timedelta
from essential_generators import DocumentGenerator
import re

products = pd.read_csv('data/products_large.csv')
buyers = pd.read_csv('data/buyers_large.csv')

def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

d = DocumentGenerator()

ratings = pd.DataFrame(columns = ['buyer_id','product_id','rating','time_reviewed','description'])
for i in range(1,500):
    buyer_id = i
    for i in range(3):
        product_id = random.randint(1,len(products))
        rating = random.randint(0,5)
        time_reviewed = gen_datetime().strftime("%m-%d-%Y %H:%M:%S")
        description = d.sentence()
        description = re.sub(r'[^\w\s]', '', description)
        description = description.replace("\n", " ")
        new_row = {'buyer_id':buyer_id,'product_id':product_id, 'rating':rating, 'time_reviewed':time_reviewed, 'description':description}
        ratings = ratings.append(new_row, ignore_index = True)

ratings.to_csv('data/product_ratings_large.csv', header = False, index = False)