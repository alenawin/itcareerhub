import pymysql
import os
from dotenv import load_dotenv


# Take from .env
load_dotenv()

mysql_config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "charset": os.getenv("MYSQL_CHARSET")
}
connection = pymysql.connect(**mysql_config)


def get_year_range(genre: str) -> (int, int):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT MIN(release_year), MAX(release_year) FROM film
        JOIN film_category ON film.film_id = film_category.film_id
        JOIN category ON category.category_id = film_category.category_id
        where category.name = %s 
        """, [genre])
        for row in cursor:
            return row


def get_categories() -> list:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM category")
        categories = [row[0].lower() for row in cursor]
    return categories


def get_films_by_keyword(keyword: str) -> list:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT title, description, release_year FROM film WHERE title LIKE %s",
            f"%{keyword}%"
        )
        films = [row for row in cursor]
    return films


def get_films_by_genre_year(genre: str, min_year: int, max_year: int) -> list:
    query = """SELECT film.title, film.description, film.release_year AS genre
        FROM film
        JOIN film_category ON film.film_id = film_category.film_id
        JOIN category ON category.category_id = film_category.category_id where """
    params = {'genre': genre}
    conditions = ["category.name = %(genre)s"]
    if max_year:
        conditions.append('film.release_year <= %(max_year)s')
        params['max_year'] = max_year
    if min_year:
        conditions.append('film.release_year >= %(min_year)s')
        params['min_year'] = min_year

    query += ' and '.join(conditions)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        films = [row for row in cursor]
    return films


def close_connection():
    connection.close()

