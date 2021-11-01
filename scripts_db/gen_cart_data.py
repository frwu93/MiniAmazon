import pandas as pd
import random

buyers = pd.read_csv('data/buyers_large.csv')
products = pd.read_csv('data/products_large.csv')

cart = pd.DataFrame(columns = ['buyer_id','product_id','quantity'])
for i in range(1,len(buyers)+1):
    buyer_id = i
    for i in range(3):
        product_id = random.randint(1,len(products))
        quantity = random.randint(1,5)
        new_row = {'buyer_id':buyer_id, 'product_id':product_id, 'quantity':quantity}
        cart = cart.append(new_row, ignore_index = True)

cart.to_csv('data/cart_large.csv', header = False, index = False)