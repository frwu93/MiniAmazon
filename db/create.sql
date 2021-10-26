-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL
);

CREATE TABLE Buyers (
    id INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES Users(id)
);

CREATE TABLE Sellers (
    id INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES Users(id)
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255),
    imageLink VARCHAR(255),
    category VARCHAR NOT NULL,
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Sells (
    seller_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (seller_id, product_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Seller_Rating (
    seller_id INT NOT NULL,
    buyer_id INT NOT NULL,
    rating INT NOT NULL,
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    CHECK(rating in (0, 1, 2, 3, 4, 5)),
    FOREIGN KEY (seller_id) REFERENCES Sellers(id),
    FOREIGN KEY (buyer_id) REFERENCES Buyers(id),
    PRIMARY KEY (buyer_id, seller_id)
);

CREATE TABLE Cart (
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES Buyers(id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    PRIMARY KEY (buyer_id, product_id)
);

CREATE TABLE Product_Rating (
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES Buyers(id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    rating INT NOT NULL,
    CHECK(rating in (0, 1, 2, 3, 4, 5)),
    time_reviewed timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    description VARCHAR(255), 
    PRIMARY KEY (buyer_id, product_id)
);

CREATE TABLE Order_History (
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES Buyers(id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    quantity INT NOT NULL,
    PRIMARY KEY (buyer_id, product_id, time_purchased)
);
