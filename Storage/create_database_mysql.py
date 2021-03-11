import mysql.connector
db_conn = mysql.connector.connect(host="messaging.eastus2.cloudapp.azure.com",port="3306", user="user", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE book_ride
          (ride_id VARCHAR(250) NOT NULL, 
          pickup_location VARCHAR(250) NOT NULL,
          destination_address VARCHAR(250) NOT NULL,
          pickup_notes VARCHAR(250) NOT NULL, 
          date_created VARCHAR(100) NOT NULL,
          CONSTRAINT ride_id_pk PRIMARY KEY (ride_id) )''')

db_cursor.execute('''
          CREATE TABLE order_food
          (order_id VARCHAR(250) NOT NULL , 
           restaurant_name VARCHAR(250) NOT NULL,
           drop_off_address VARCHAR(250) NOT NULL,
           drop_off_instructions VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT order_id_pk PRIMARY KEY(order_id)
           )''')


db_conn.commit()
db_conn.close()