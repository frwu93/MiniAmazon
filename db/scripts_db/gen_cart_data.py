import pandas as pd
import random
from faker import Faker

Faker.seed(0)
fake = Faker()

users = pd.read_csv('./data/Users_large.csv', header = None)
products = pd.read_csv('./data/Products_large.csv', header = None)
cart = pd.DataFrame(columns = ['buyer_id','product_id','quantity', 'saved'])
for i in range(1,len(users)+1):
    print(i)
    buyer_id = i
    for j in range(5):
        product_id = fake.random_int(min=1, max=len(products)-1)
        quantity = random.randint(1,5)
        saved = fake.boolean(chance_of_getting_true = 25)
        new_row = {'buyer_id':buyer_id, 'product_id':product_id, 'quantity':quantity, 'saved':saved}
        cart = cart.append(new_row, ignore_index = True)
cart = cart.drop_duplicates(subset = ['buyer_id', 'product_id'])

cart.to_csv('./data/Cart_large.csv', header = False, index = False)