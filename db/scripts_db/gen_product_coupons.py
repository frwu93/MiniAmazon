import pandas as pd
import random
from faker import Faker

Faker.seed(0)
fake = Faker()

pcs = pd.DataFrame(columns = ['coupon_code','product_id'])
coupons = pd.read_csv('./data/Coupons_large.csv', header = None)
products = pd.read_csv('./data/Products_large.csv', header = None)


for i in range(500):
    coupon_code = coupons.iloc[fake.random_int(min=0, max=len(coupons)-1),0]
    product_id = products.iloc[fake.random_int(min=0, max=len(products)-1),0]
    new_row = {'coupon_code': coupon_code, 'product_id':product_id}
    pcs = pcs.append(new_row, ignore_index = True)
pcs = pcs.drop_duplicates(subset = ['coupon_code'])
pcs.to_csv('./data/Product_Coupons_large.csv', header = False, index = False)