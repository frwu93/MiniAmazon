\COPY Users (email, password, firstname, lastname, balance) FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Buyers FROM 'data/Buyers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Sellers FROM 'data/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products (name, description, imageLink,category, price, available)FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Sells FROM 'data/Sells.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller_Rating FROM 'data/Seller_Rating.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Cart FROM 'data/Cart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product_Rating FROM 'data/Product_Rating.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Order_History FROM 'data/Order_History.csv' WITH DELIMITER ',' NULL '' CSV
