-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL
);

CREATE TABLE Sellers (
    id INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES Users(id)
);

CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255),
    imageLink VARCHAR(255),
    category VARCHAR NOT NULL,
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    quantity INT NOT NULL,
    FOREIGN KEY (seller_id) REFERENCES Sellers(id)
);

CREATE TABLE Seller_Rating (
    seller_id INT NOT NULL,
    buyer_id INT NOT NULL,
    rating INT NOT NULL,
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    CHECK(rating in (0, 1, 2, 3, 4, 5)),
    FOREIGN KEY (seller_id) REFERENCES Sellers(id),
    FOREIGN KEY (buyer_id) REFERENCES Users(id),
    PRIMARY KEY (buyer_id, seller_id)
);

CREATE TABLE Cart (
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES Users(id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    PRIMARY KEY (buyer_id, product_id)
);

CREATE TABLE Product_Rating (
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES Users(id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    rating INT NOT NULL,
    CHECK(rating in (0, 1, 2, 3, 4, 5)),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    description VARCHAR(255), 
    PRIMARY KEY (buyer_id, product_id)
);

CREATE TABLE Orders(
    order_id SERIAL PRIMARY KEY,
    buyer_id INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES Users(id),
    time_ordered timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Order_History (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    price FLOAT NOT NULL,
    quantity INT NOT NULL,
    fulfilled BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (product_id, order_id)
);
