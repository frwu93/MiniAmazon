import pandas as pd 
from faker import Faker
from werkzeug.security import generate_password_hash

Faker.seed(0)
fake = Faker()
df = pd.DataFrame(columns=['email','password','firstname','lastname','address','balance'])

for i in range(1001):
    first = fake.first_name()
    last = fake.last_name()
    email = fake.unique.ascii_free_email() 
    password = generate_password_hash(first+last)
    address = fake.address()
    balance = fake.random_int(min=0, max=10000)
    new_row = {'email': email, 'password': password, 'firstname':first,'lastname':last,'address': address,'balance':float(balance)}
    df = df.append(new_row, ignore_index=True)
    print(i)
df.to_csv('./data/Users_large.csv', header = False, index = False)