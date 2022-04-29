# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists Users;")
cursor.execute("drop table if exists Sensor_Data;")
cursor.execute("drop table if exists Login_Data;")

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE Users (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      first_name  VARCHAR(30) NOT NULL,
      last_name   VARCHAR(30) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      focus    VARCHAR(20) NOT NULL,
      created_at  TIMESTAMP
    );
  """)
except:
  print("Users table already exists. Not recreating it.")

try:
  cursor.execute("""
    CREATE TABLE Sensor_Data (
      id                integer  AUTO_INCREMENT PRIMARY KEY,
      username          VARCHAR(30) NOT NULL,
      password          VARCHAR(30) NOT NULL,
      pir               integer NOT NULL,
      vib               integer NOT NULL,
      ax                integer NOT NULL,
      ay                integer NOT NULL,
      az                integer NOT NULL,
      lat               float NOT NULL,
      long              float NOT NULL,
      time              TIMESTAMP
    );
  """)
except:
  print("Sensor_Data table already exists. Not recreating it.")

try:
  cursor.execute("""
    CREATE TABLE Login_Data (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      username    VARCHAR(30) NOT NULL,
      password    VARCHAR(30) NOT NULL
    );
  """)
except:
  print("Login_Data table already exists. Not recreating it.")

# Insert Records
query = "insert into Users (first_name, last_name, email, focus) values (%s, %s, %s, %s)"
values = [
  ('Girish','Krishnan','gikrishnan@ucsd.edu', 'Software Dev'),
  ('Anish','Sharma','ans019@ucsd.edu', 'Circuit Design'),
  ('Hamza','Khan','hmk018@ucsd.edu', 'Customer Rep'),
  ('Ian','Tanuwidjaja','itanuwidjaja@ucsd.edu', 'Financial Exec')
]
cursor.executemany(query, values)

query = "insert into Login_Data (username,password) values (%s, %s)"
values = [
  ('myesp32_1234','thisisanesp32')
]
cursor.executemany(query, values)

db.commit()

# Selecting Records
# cursor.execute("select * from Users;")
# print('---------- DATABASE INITIALIZED ----------')
# [print(x) for x in cursor]
db.close()
