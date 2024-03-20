import mysql.connector
from flask import Flask
app = Flask(__name__)
import pdb

# input_str here is the url to be shortened
def decimal_to_base62(decimal):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base62 = ""

    while decimal > 0:
        remainder = decimal % 62
        base62 = characters[remainder] + base62
        decimal //= 62

    return base62 if base62 else "0"

def insert_data(input_str, unique_integer):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Bits@1612",
            database="my_database"
        )

        cursor = connection.cursor()

        sql = "INSERT INTO input_data (input_str, unique_integer) VALUES (%s, %s)"
        val = (input_str, unique_integer)
        cursor.execute(sql, val)

        connection.commit()
        print("Data inserted successfully.")

    except mysql.connector.Error as error:
        print("Failed to insert data into MySQL table:", error)

    finally:
        if 'connection' in locals():
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")
                
def fetch_data(short_url):
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Bits@1612",
        database="my_database"
    )

    cursor = connection.cursor()

    sql = "select input_str from input_data where unique_integer=\"{}\"".format(short_url) 
    cursor.execute(sql)
    print(sql)
      
    print("Data fetched successfully.")
    for row in cursor:
        print(row) 
        
    return row[0]

@app.route('/')
def hello():
    return "Hello World! I am up!"

@app.route('/<name>')
def new_hello(name):
    return "Hello {}".format(name)

@app.route('/shorten/<long_url>')              
def shorten_url(long_url):
    hash_value = hash(long_url)
    string_length = len(long_url)
    combined_hash = hash_value ^ (string_length << 16) ^ string_length
    unique_integer = combined_hash % 238000
    short_url = decimal_to_base62(unique_integer)
    insert_data(long_url, short_url)
    return short_url
    
@app.route('/fetch/<short_url>')
def fetch(short_url):
    # lookup short_url from DB and return long_url
    # pdb.set_trace()
    return fetch_data(short_url)
    

if __name__ == "__main__":
    app.run()

