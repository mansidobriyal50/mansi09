import flask
from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)  

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'blogging_platform'
}

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT posts.id, posts.title, users.username AS author_name
                FROM posts
                JOIN users ON posts.author_id = users.id
            """)
            posts = cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            posts = []
        finally:
            cursor.close()
            connection.close()
    else:
        posts = []
    return render_template('my_html.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=False)



