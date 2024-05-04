from flask import Flask, render_template, request
import psycopg2
from scraper import fetch_movies  # Import the scraping function

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="movies",
        user="postgres",
        password="jinjin.")
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update_database():
    movies = fetch_movies()
    conn = get_db_connection()
    cur = conn.cursor()
    for title, release_date, rating in movies:
        # Check if the movie already exists
        cur.execute('SELECT * FROM movies WHERE title = %s AND release_date = %s', (title, release_date))
        exists = cur.fetchone()
        if not exists:
            cur.execute('INSERT INTO movies (title, release_date, ratings) VALUES (%s, %s, %s)', (title, release_date, rating))
    conn.commit()
    cur.close()
    conn.close()
    return "Database Updated!"

@app.route('/random', methods=['GET', 'POST'])
def random_movies():
    num = int(request.form.get('number', 5))  # Default to 5 if no input
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT title, ratings FROM movies ORDER BY random() LIMIT %s', (num,))
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('movies.html', movies=movies)

@app.route('/top', methods=['GET', 'POST'])
def top_movies():
    num = int(request.form.get('number', 5))  # Default to 5 if no input
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT title, ratings FROM movies ORDER BY ratings DESC LIMIT %s', (num,))
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('movies.html', movies=movies)

# Other routes will be added for future implementation

if __name__ == '__main__':
    app.run(debug=True)