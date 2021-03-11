import sqlite3

conn = sqlite3.connect('requests.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE book_ride
          (ride_id VARCHAR PRIMARY KEY ASC, 
          pickup_location VARCHAR(250) NOT NULL,
          destination_address VARCHAR(250) NOT NULL,
          pickup_notes VARCHAR(250) NOT NULL, 
          date_created VARCHAR(100) NOT NULL)
          
          ''')

c.execute('''
          CREATE TABLE order_food
          (order_id VARCHAR PRIMARY KEY ASC, 
           restaurant_name VARCHAR(250) NOT NULL,
           drop_off_address VARCHAR(250) NOT NULL,
           drop_off_instructions VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL
           )
          ''')

conn.commit()
conn.close()
