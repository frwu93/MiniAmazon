import pandas as pd 
from faker import Faker
from string import punctuation


Faker.seed(0)
fake = Faker()
sellers = pd.read_csv('./data/Sellers_large.csv', header = None)

df = pd.DataFrame(columns=['product_id','seller_id', 'name','description','imageLink','category','price','available','quantity'])

cats = ['Clothing', 'Accessories', 'Books','Entertainment', 'Electronics', 'Home', 'Pet Supplies', 'Food', 'Beauty', 'Toys', 'Sports', 'Outdoors', 'Automotives', 'Other']
for i in range(1,10001):
    print(i)
    product_id = i
    seller_id = sellers.iloc[fake.random_int(min=0, max=len(sellers)-1),0]
    name = fake.sentence(nb_words = 4).title().strip(punctuation)
    description = fake.paragraph(nb_sentences=5)
    imageLink = fake.image_url()
    category = fake.word(ext_word_list = cats)
    price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
    avail = fake.boolean(chance_of_getting_true=80)
    quantity = fake.random_int(min = 5, max=1000)
    new_row = {'product_id':product_id, 'seller_id':seller_id,'name': name, 'description': description, 'imageLink':imageLink,'category':category,'price':price, 'available':avail, 'quantity' :quantity}
    df = df.append(new_row, ignore_index=True)

df.to_csv('data/Products_large.csv', header = False, index = False)