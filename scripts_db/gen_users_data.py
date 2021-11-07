#to run this, run "pip install names" in terminal

import pandas as pd 
import names
import random 
from werkzeug.security import generate_password_hash


df = pd.DataFrame(columns=['email','password','firstname','lastname','balance'])

for i in range(1001):
    first = names.get_first_name()
    last = names.get_last_name()
    email = first+last+'@gmail.com'
    password = generate_password_hash(first+last)
    balance = random.randint(0,1000)
    new_row = {'email': email, 'password': password, 'firstname':first,'lastname':last,'balance':float(balance)}
    df = df.append(new_row, ignore_index=True)

df.to_csv('data/users_large.csv', header = False, index = False)