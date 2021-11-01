import pandas as pd 
import random 
from random_word import RandomWords
from essential_generators import DocumentGenerator
import re

df = pd.DataFrame(columns=['name','description','imageLink','category','price','available'])

r = RandomWords()
d = DocumentGenerator()
cats = ["food","clothing","electronics","furniture","decor"]
for i in range(1001):
    print(i)
    name = r.get_random_word(includePartOfSpeech="noun")
    description = d.sentence()
    description = re.sub(r'[^\w\s]', '', description)
    description = description.replace("\n", " ")
    imageLink = d.url()
    category = cats[random.randint(0,4)]
    price = round(random.uniform(0.00, 5000.00), 2)
    avail = bool(random.getrandbits(1))
    if (avail):
        avail = "TRUE"
    else:
        avail = "FALSE"
    new_row = {'name': name, 'description': description, 'imageLink':imageLink,'category':category,'price':price, 'available':avail}
    df = df.append(new_row, ignore_index=True)

df.to_csv('data/products_large.csv', header = False, index = False)