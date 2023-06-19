DROP TABLE IF EXISTS purchase_items;
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS price_change;
DROP TABLE IF EXISTS material;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS color;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS customers;

CREATE TABLE material
(
    material_id INT NOT NULL PRIMARY KEY, 
    material VARCHAR(50) NOT NULL
);

CREATE TABLE categories
(
    category_id INT NOT NULL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
);

CREATE TABLE color
(
    color_id INT NOT NULL PRIMARY KEY,
    color VARCHAR(50) NOT NULL,
);


CREATE TABLE products (
    product_id INT Primary Key,
    product_name VARCHAR(255) NOT NULL,
    category_id INT,
    material_id INT,
    color_id INT,
    FOREIGN KEY (category_id) REFERENCES categories (category_id),
    FOREIGN KEY (material_id) REFERENCES material (material_id),
    FOREIGN KEY (color_id) REFERENCES color (color_id)
);


CREATE TABLE price_change
(
    product_id INT,
    data_price_change DATE NOT NULL,
    new_price money NOT NULL,
    CONSTRAINT PK_PRICE_CHANGE PRIMARY KEY (product_id, date_price_change),  
    FOREIGN key (product_id) REFERENCES products (product_id)
);

CREATE TABLE purchases_item
(
    purchase_id INT PRIMARY KEY,
    product_id INT,
    product_count INT NOT NULL,
    product_price money NOT NULL,
    CONSTRAINT PK_PURCHASE_ITEMS PRIMARY KEY (purchase_id, product_id),  
    FOREIGN key (product_id) REFERENCES products (product_id)
);

CREATE TABLE purchases
(
    purchase_id INT PRIMARY KEY,
    customer_id INT,
    purchase_date  DATE,
    FOREIGN key (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE customers
(
    customer_id INT PRIMARY KEY,
    customer_fname VARCHAR(30),
    customer_lname VARCHAR(30),
    phone VARCHAR(13),
    telegram_serial VARCHAR,
);

