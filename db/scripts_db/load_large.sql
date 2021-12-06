\COPY Users (email, password, firstname, lastname, address, balance) FROM './data/Users_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Sellers FROM './data/Sellers_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM './data/Products_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller_Rating FROM './data/Seller_Rating_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Cart FROM './data/Cart_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product_Rating FROM './data/Product_Rating_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Orders  FROM './data/Orders_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Order_History FROM './data/Order_History_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Coupons FROM './data/Coupons_large.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product_Coupons FROM './data/Product_Coupons_large.csv' WITH DELIMITER ',' NULL '' CSV
