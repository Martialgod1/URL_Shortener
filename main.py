import mysql.connector
import random
import string

from flask import Flask, request, jsonify, render_template
import hashlib

app = Flask(__name__)

def decimal_to_base62(decimal):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base62 = ""

    while decimal > 0:
        remainder = decimal % 62
        base62 = characters[remainder] + base62
        decimal //= 62

    # Ensure the output is of fixed length (3 characters in this case)
    base62 = base62.rjust(3, '0')[:3]  # Right justify and take first 3 characters

    return base62


def hash_url(url):
    # Use a proper hashing algorithm like SHA-256
    return hashlib.sha256(url.encode()).hexdigest()

def insert_data(input_str, short_url):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root1234",
            database="my_database"
        )

        cursor = connection.cursor()

        sql = "INSERT INTO input_data (input_str, unique_integer) VALUES (%s, %s)"  # corrected column name
        val = (input_str, short_url)
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
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root1234",
            database="my_database"
        )

        cursor = connection.cursor()

        sql = "SELECT input_str FROM input_data WHERE unique_integer = %s"  # corrected column name
        cursor.execute(sql, (short_url,))
        print(sql)

        print("Data fetched successfully.")
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return "URL not found"

    except mysql.connector.Error as error:
        print("Failed to fetch data from MySQL table:", error)
        return "Error"

    finally:
        if 'connection' in locals():
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']
    url_hash = hash_url(long_url)
    decimal_representation = int(url_hash, 16)
    short_url = decimal_to_base62(decimal_representation)
    insert_data(long_url, short_url)
    return jsonify({'result': short_url})


@app.route('/fetch', methods=['POST'])
def fetch():
    short_url = request.form['url']
    long_url = fetch_data(short_url)
    return jsonify({'result': long_url})

if __name__ == "__main__":
    app.run(debug=True)
