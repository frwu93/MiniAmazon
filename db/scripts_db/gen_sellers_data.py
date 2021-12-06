import pandas as pd

users = pd.read_csv('data/users_large.csv')

sellers = pd.DataFrame(columns = ['id'])
for i in range(1,500):
    new_row = {'id':i}
    sellers = sellers.append(new_row, ignore_index = True)

sellers.to_csv('data/sellers_large.csv', header = False, index = False)