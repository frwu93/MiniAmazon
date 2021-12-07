\COPY Users (email, password, firstname, lastname, address, balance) FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Sellers FROM 'data/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products (seller_id, name, description, imageLink,category, price, available, quantity)FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller_Rating FROM 'data/Seller_Rating.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Cart FROM 'data/Cart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product_Rating FROM 'data/Product_Rating.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Orders (buyer_id, total_cost, time_ordered, coupon_used) FROM 'data/Orders.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Order_History FROM 'data/Order_History.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Coupons FROM 'data/Coupons.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product_Coupons FROM 'data/Product_Coupons.csv' WITH DELIMITER ',' NULL '' CSV
