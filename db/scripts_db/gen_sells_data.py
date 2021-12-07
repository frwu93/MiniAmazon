import pandas as pd
import random

sellers = pd.read_csv('data/sellers_large.csv')
products = pd.read_csv('data/products_large.csv')

sells = pd.DataFrame(columns = ['seller_id','product_id','quantity'])
for i in range(1,500):
    seller_id = i
    for i in range(3):
        product_id = random.randint(1,len(products))
        quantity = random.randint(1,10)
        new_row = {'seller_id':seller_id, 'product_id':product_id, 'quantity':quantity}
        sells = sells.append(new_row, ignore_index = True)

sells.to_csv('data/sells_large.csv', header = False, index = False)