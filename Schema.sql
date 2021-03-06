create database bookstoredb;
USE bookstoredb;

CREATE TABLE book (
  isbn10 CHAR(10) PRIMARY KEY,
  title VARCHAR(256) NOT NULL,
  authors VARCHAR(256),
  publisher VARCHAR(64),
  year INT, #format YYYY
  stock INT NOT NULL CHECK (stock>=0),
  format ENUM('paperback','hardcover'),
  subject VARCHAR(64)
);

CREATE TABLE customer(
  login_name VARCHAR(10) PRIMARY KEY,
  full_name VARCHAR(64),
  password VARCHAR(16),
  credit_card VARCHAR(16),
  address VARCHAR(256),
  phone INT(8)
);

#####################################################
## Run this line
ALTER TABLE customer MODIFY credit_card VARCHAR(16); 
#####################################################

CREATE TABLE feedback(
  entry_date DATE,
  score INT not null check(score>=0 and score<=10),
  opinion VARCHAR(256),
  login_name VARCHAR(10),
  isbn10 CHAR(10),
  PRIMARY KEY (login_name, isbn10),
  FOREIGN KEY (login_name) REFERENCES customer(login_name),
  FOREIGN KEY (isbn10) REFERENCES book(isbn10)
  #participation constraint of one user one book feedback
);

CREATE TABLE usefulness_rating(
  rater VARCHAR(10),
  usefulness INT not null check(score>=0 and score<=2),
  user VARCHAR(10),
  isbn10 CHAR(10),
  PRIMARY KEY (rater, user, isbn10),
  FOREIGN KEY (rater) REFERENCES customer(login_name),
  FOREIGN KEY (user) REFERENCES customer(login_name),
  FOREIGN KEY (isbn10) REFERENCES book(isbn10)
  #need to add constraint to ensure rater != user
);

CREATE TABLE order_history(
  oid INT(6),
  order_date DATE,
  order_status VARCHAR(256),
  PRIMARY KEY (oid)
);

CREATE TABLE ordering(
  login_name VARCHAR(10),
  oid INT(6),
  PRIMARY KEY (login_name, oid),
  FOREIGN KEY (login_name) REFERENCES customer(login_name),
  FOREIGN KEY (oid) REFERENCES order_history(oid)
);

CREATE TABLE books_ordered(
  oid INT(6),
  isbn10 CHAR(10),
  quantity INT not null check(quantity>0),
  PRIMARY KEY (oid,isbn10),
  FOREIGN KEY (isbn10) REFERENCES book(isbn10),
  FOREIGN KEY (oid) REFERENCES order_history(oid)
);
