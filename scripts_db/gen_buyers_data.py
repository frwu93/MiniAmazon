import pandas as pd

users = pd.read_csv('data/users_large.csv')

buyers = pd.DataFrame(columns = ['id'])
for i in range(1,len(users)+1):
    new_row = {'id':i}
    buyers = buyers.append(new_row, ignore_index = True)

buyers.to_csv('data/buyers_large.csv', header = False, index = False)
