# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Book(models.Model):
    isbn10 = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=256)
    authors = models.CharField(max_length=256, blank=True, null=True)
    publisher = models.CharField(max_length=64, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    stock = models.PositiveIntegerField()
    formatchoices = (
        ('paperback', 'paperback'),
        ('hardcover', 'hardcover')
    )
    format = models.CharField(max_length=9, blank=True, null=True, choices=formatchoices)
    subject = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'

# CREATE TABLE book (
#   isbn10 CHAR(10) PRIMARY KEY,
#   title VARCHAR(256) NOT NULL,
#   authors VARCHAR(256),
#   publisher VARCHAR(64),
#   year INT, #format YYYY
#   stock INT NOT NULL CHECK (stock>=0),
#   format ENUM('paperback','hardcover'),
#   subject VARCHAR(64)
# );

class BooksOrdered(models.Model):
    oid = models.ForeignKey(OrderHistory, models.DO_NOTHING, db_column='oid')
    isbn10 = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn10')
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'books_ordered'
        unique_together = (('oid', 'isbn10'),)

# CREATE TABLE books_ordered(
#   oid INT(6),
#   isbn10 CHAR(10),
#   quantity INT not null check(quantity>0),
#   PRIMARY KEY (oid,isbn10),
#   FOREIGN KEY (isbn10) REFERENCES book(isbn10),
#   FOREIGN KEY (oid) REFERENCES order_history(oid)
# );

class Customer(models.Model):
    login_name = models.CharField(primary_key=True, max_length=10)
    full_name = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=16, blank=True, null=True)
    credit_card = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'

# CREATE TABLE customer(
#   login_name VARCHAR(10) PRIMARY KEY,
#   full_name VARCHAR(64),
#   password VARCHAR(16),
#   credit_card INT(16),
#   address VARCHAR(256),
#   phone INT(8)
# );

class Feedback(models.Model):
    entry_date = models.DateField(blank=True, null=True)
    scorechoices = zip(range(1,10), range(1,10))
    score = models.IntegerField(choices=scorechoices)
    opinion = models.CharField(max_length=256, blank=True, null=True)
    login_name = models.ForeignKey(Customer, models.DO_NOTHING, db_column='login_name')
    isbn10 = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn10')

    class Meta:
        managed = False
        db_table = 'feedback'
        unique_together = (('login_name', 'isbn10'),)

# CREATE TABLE feedback(
#   entry_date DATE,
#   score INT not null check(score>=0 and score<=10),
#   opinion VARCHAR(256),
#   login_name VARCHAR(10),
#   isbn10 CHAR(10),
#   PRIMARY KEY (login_name, isbn10),
#   FOREIGN KEY (login_name) REFERENCES customer(login_name),
#   FOREIGN KEY (isbn10) REFERENCES book(isbn10)
#   #participation constraint of one user one book feedback
# );


class OrderHistory(models.Model):
    oid = models.IntegerField(primary_key=True)
    order_date = models.DateField(blank=True, null=True)
    order_status = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_history'

# CREATE TABLE order_history(
#   oid INT(6),
#   order_date DATE,
#   order_status VARCHAR(256),
#   PRIMARY KEY (oid)
# );


class Ordering(models.Model):
    login_name = models.ForeignKey(Customer, models.DO_NOTHING, db_column='login_name')
    oid = models.ForeignKey(OrderHistory, models.DO_NOTHING, db_column='oid')

    class Meta:
        managed = False
        db_table = 'ordering'
        unique_together = (('login_name', 'oid'),)

# CREATE TABLE ordering(
#   login_name VARCHAR(10),
#   oid INT(6),
#   PRIMARY KEY (login_name, oid),
#   FOREIGN KEY (login_name) REFERENCES customer(login_name),
#   FOREIGN KEY (oid) REFERENCES order_history(oid)
# );


class UsefulnessRating(models.Model):
    rater = models.ForeignKey(Customer, models.DO_NOTHING, db_column='rater')
    usefulness = models.IntegerField()
    user = models.ForeignKey(Customer, models.DO_NOTHING, db_column='user')
    isbn10 = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn10')

    class Meta:
        managed = False
        db_table = 'usefulness_rating'
        unique_together = (('rater', 'user', 'isbn10'),)

# CREATE TABLE usefulness_rating(
#   rater VARCHAR(10),
#   usefulness INT not null check(score>=0 and score<=2),
#   user VARCHAR(10),
#   isbn10 CHAR(10),
#   PRIMARY KEY (rater, user, isbn10),
#   FOREIGN KEY (rater) REFERENCES customer(login_name),
#   FOREIGN KEY (user) REFERENCES customer(login_name),
#   FOREIGN KEY (isbn10) REFERENCES book(isbn10)
#   #need to add constraint to ensure rater != user
# );
