import mysql.connector
import logging

class DatabaseManager:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            logging.info("Connected to database successfully!")
        except mysql.connector.Error as e:
            logging.error(f"Error connecting to database: {e}")
            raise e

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logging.info("Connection closed.")

    def execute_query(self, query, values=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            logging.error(f"Error executing query: {e}")
            return False
        finally:
            cursor.close()

    def fetch_all(self, query, values=None):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, values)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            logging.error(f"Error fetching data: {e}")
            return []
        finally:
            cursor.close()

class DataManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def insert_user(self, username, email, password, bio=''):
        query = "INSERT INTO users (username, email, password, bio) VALUES (%s, %s, %s, %s)"
        values = (username, email, password, bio)
        return self.db_manager.execute_query(query, values)

    def insert_post(self, title, content, author_id):
        query = "INSERT INTO posts (title, content, author_id) VALUES (%s, %s, %s)"
        values = (title, content, author_id)
        return self.db_manager.execute_query(query, values)

    def insert_follower(self, follower_id, following_id):
        query = "INSERT INTO followers (follower_id, following_id) VALUES (%s, %s)"
        values = (follower_id, following_id)
        return self.db_manager.execute_query(query, values)
    
    def insert_comment(self, content, post_id, author_id):
        query = "INSERT INTO comments (content, post_id, author_id) VALUES (%s, %s, %s)"
        values = (content, post_id, author_id)
        return self.db_manager.execute_query(query, values)

    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.db_manager.fetch_all(query)

    def get_all_posts(self):
        query = "SELECT * FROM posts"
        return self.db_manager.fetch_all(query)

    def get_all_comments(self):
        query = "SELECT * FROM comments"
        return self.db_manager.fetch_all(query)

    def get_posts_with_authors(self):
        query = """
        SELECT posts.*, users.username AS author_username, users.email AS author_email
        FROM posts
        JOIN users ON posts.author_id = users.id;
        """
        return self.db_manager.fetch_all(query)

    def get_comments_with_posts_and_authors(self):
        query = """
        SELECT comments.*, posts.title AS post_title, users.username AS author_username
        FROM comments
        JOIN posts ON comments.post_id = posts.id
        JOIN users ON comments.author_id = users.id;
        """
        return self.db_manager.fetch_all(query)

def main():
    # Database connection parameters
    db_host = 'localhost'
    db_username = 'root'
    db_password = 'root'
    db_name = 'blogging_platform'

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        with DatabaseManager(host=db_host, username=db_username, password=db_password, database=db_name) as db_manager:
            data_manager = DataManager(db_manager)

            # Insert users
            users_to_insert = [
                ("mansi", "mansidobriyal50@gmail.com", "mansi1234", "happy girl"),
                ("manav", "manav22@gmail.com", "manav1234", "nightmare"),
                ("kailash", "kailashchand25@gmail.com", "kailash1234", "humour is first priority"),
                ("rashmi", "rashmi11@gmail.com", "rashmi1234", "mum of a pretty girl")
            ]
            for user in users_to_insert:
                success = data_manager.insert_user(*user)
                if success:
                    logging.info(f"User {user[0]} inserted successfully!")
                else:
                    logging.error(f"Failed to insert user {user[0]}.")

            # Insert new posts
            posts_to_insert = [
                ("Blooming Flower", "Flowers are the vibrant, colorful, and fragrant reproductive structures of flowering plants. They are nature's way of attracting pollinators, such as bees, butterflies, and birds, ensuring the continuation of plant species through the process of pollination. Beyond their biological purpose, flowers hold a special place in human culture and emotions. They are symbols of beauty, love, and life, often given as gifts to express affection, sympathy, and congratulations. Each type of flower carries its own unique symbolism and aesthetic appeal, making them integral to gardens, celebrations, and rituals around the world. From the delicate petals of a rose to the bright faces of sunflowers, flowers bring joy and serenity, reminding us of the intricate beauty of the natural world.", 1),  # Assuming author ID 1 exists
                ("Night Sky", "The night sky is a breathtaking canvas of cosmic wonders, captivating viewers with its serene and mysterious beauty. As the sun sets and darkness envelops the earth, the sky transforms into a vast expanse studded with shimmering stars, distant planets, and the gentle glow of the moon. A picture of the night sky can evoke a sense of wonder and tranquility, capturing the delicate twinkle of countless stars that have traveled light-years to reach our eyes. The constellations, with their storied histories, trace patterns that have guided travelers and inspired dreamers for millennia. The deep, velvety blackness is occasionally interrupted by the streak of a meteor or the slow, deliberate march of a satellite. In rural areas, far from city lights, the night sky reveals even more of its secrets, with the Milky Way's hazy band arching gracefully across the heavens. Whether observed through the lens of a camera or the naked eye, the night sky is a profound reminder of the universe's vastness and the enduring beauty of the cosmos.", 2),
                ("Humorous Moments", "A humorous moment captured in a picture, where everyone is in joy, radiates pure delight and camaraderie. The photograph might show a group of friends or family members in the midst of laughter, their faces lit up with smiles and eyes sparkling with mirth. Perhaps someone just told a hilarious joke, or a playful mishap occurred, igniting a wave of contagious laughter. The spontaneous expressions and animated gestures in the image reflect a shared experience of joy and light-heartedness. Such moments are treasures, as they highlight the bonds between people and the simple, yet profound, happiness found in each other's company. Whether it’s the result of a funny story, a witty comment, or an unexpected twist, these humorous moments bring people together, creating memories that are cherished long after the laughter fades.", 3),
                ("Motherhood", "A picture capturing the essence of motherhood reveals a profound bond of love and tenderness between a mother and her child. In this snapshot, the mother's face beams with a radiant smile, her eyes filled with a deep sense of fulfillment and unconditional affection. Cradling her child in her arms or gazing adoringly at them, she exudes a warmth that transcends words. It's a moment where every touch, every glance, conveys a world of emotions—joy, pride, and an overwhelming sense of responsibility. The child, nestled close, embodies trust and security in the embrace of their nurturing guardian. This picture epitomizes the beauty of motherhood, a journey of selfless devotion and endless nurturing, where each moment is a testament to the boundless love that shapes both mother and child.", 4)
            ]
            for post in posts_to_insert:
                success = data_manager.insert_post(*post)
                if success:
                    logging.info(f"Post '{post[0]}' by Author ID {post[2]} inserted successfully!")
                else:
                    logging.error(f"Failed to insert post '{post[0]}'.")

            # Insert new follower relationships
            followers_to_insert = [
                (1, 2),  # Assuming follower and following IDs exist
                (2, 3),
                (3, 4),
                (4, 1)
            ]
            for follower in followers_to_insert:
                success = data_manager.insert_follower(*follower)
                if success:
                    logging.info(f"Follower relationship {follower[0]} -> {follower[1]} inserted successfully!")
                else:
                    logging.error(f"Failed to insert follower relationship {follower[0]} -> {follower[1]}.")

            # Insert new comments
            comments_to_insert = [
                ("Indeed nature is beautiful and colorful like the flowers!", 1, 1),  # Comment content, post ID, author ID
                ("Aaahhh sky is my fav! and especially at night.", 2, 2),
                ("Love, Laughter and memories!", 3, 3),
                ("Greatest feeling and joy of all time!", 4, 4)
            ]
            for comment in comments_to_insert:
                success = data_manager.insert_comment(*comment)
                if success:
                    logging.info(f"Comment '{comment[0]}' inserted successfully!")
                else:
                    logging.error(f"Failed to insert comment '{comment[0]}'.")

            # Fetch and print all users
            users = data_manager.get_all_users()
            logging.info("Users:")
            for user in users:
                logging.info(user)

            # Fetch and print all posts
            posts = data_manager.get_all_posts()
            logging.info("Posts:")
            for post in posts:
                logging.info(post)

            # Fetch and print all comments
            comments = data_manager.get_all_comments()
            logging.info("Comments:")
            for comment in comments:
                logging.info(comment)

            # Fetch and print posts with author details
            posts_with_authors = data_manager.get_posts_with_authors()
            logging.info("Posts with Authors:")
            for post in posts_with_authors:
                logging.info(post)

            # Fetch and print comments with post and author details
            comments_with_details = data_manager.get_comments_with_posts_and_authors()
            logging.info("Comments with Post and Author Details:")
            for comment in comments_with_details:
                logging.info(comment)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


