import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

Faker.seed(0)
fake = Faker()


products = pd.read_csv('./data/Products_large.csv', header = None)


orders = pd.DataFrame(columns = ['order_id','product_id','price','quantity','fulfilled'])
for i in range(10000):
    print(i)
    order_id = i
    items = fake.random_int(min=1, max = 10)
    prods = []
    for j in range(items):
        filtered = products.loc[~products.iloc[:,0].isin(prods)].reset_index()
        rng = fake.random_int(min=0, max=len(filtered)-1)
        product_id = filtered.iloc[rng,1]
        price = filtered.iloc[rng,7]
        prods.append(product_id)
        quantity = random.randint(1,5)
        fulfilled = fake.boolean(chance_of_getting_true = 90)
        new_row = {'order_id':order_id, 'product_id': product_id, 'price':price, 'quantity':quantity, 'fulfilled':fulfilled}
        orders = orders.append(new_row, ignore_index = True)
orders = orders.drop_duplicates(subset = ['order_id', 'product_id'])
orders.to_csv('./data/Order_History_large.csv', header = False, index = False)