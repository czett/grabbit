import psycopg2
from psycopg2 import sql
import bcrypt
import json
from geopy.geocoders import Nominatim

with open("credentials.yml", "r") as creds:
    pw = creds.readlines()[0]

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres.dyrwvzlopsfrqekkhkuu",
    "password": pw,
    "host": "aws-0-eu-west-3.pooler.supabase.com",
    "port": 6543,
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def register(username: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed_password.decode()),
                )
        return True, "Success"
    except psycopg2.errors.UniqueViolation:
        return False, "Username already exists"
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        conn.close()

def login(username: str, password: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user and bcrypt.checkpw(password.encode(), user[0].encode()):
                return True, "Success"
            else:
                return False, "Wrong username or password"
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        conn.close()

def check_user_exists(user_id: str):
    """
    Checks if a user exists in the database by their user_id.
    
    Args:
        user_id (str): The ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE username = %s", (user_id,))
                user = cur.fetchone()

                if user:
                    return True
                else:
                    return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def get_username_by_user_id(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
            username = cur.fetchone()
            if username:
                return username[0]
            else:
                return None
    except Exception as e:
        return None

def get_user_id_by_username(username):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user:
                return user[0]
            else:
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="go2klo_app")

    location = geolocator.geocode(location_name)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None
    

def post_purchase(paid_price: float, usual_price: float, departments: list, comment: str, coords: tuple, user: str):
    latitude, longitude = coords
    conn = get_db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Prüfen, ob der Laden bereits existiert
                cur.execute(
                    """
                    SELECT store_id FROM stores
                    WHERE latitude = %s AND longitude = %s
                    """,
                    (latitude, longitude)
                )
                result = cur.fetchone()

                if result:
                    store_id = result[0]
                else:
                    # Neuen Laden eintragen (ohne store_name)
                    cur.execute(
                        """
                        INSERT INTO stores (latitude, longitude)
                        VALUES (%s, %s)
                        RETURNING store_id
                        """,
                        (latitude, longitude)
                    )
                    store_id = cur.fetchone()[0]

                # Eintrag für den Einkauf erstellen
                cur.execute(
                    """
                    INSERT INTO purchases (store_id, paid_price, usual_price, departments, comment, username)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING purchase_id
                    """,
                    (store_id, paid_price, usual_price, ', '.join(departments), comment, user)
                )
                purchase_id = cur.fetchone()[0]

                return True, f"Purchase posted successfully with ID {purchase_id} for store at ({latitude}, {longitude})"
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        conn.close()

def get_all_stores():
    conn = get_db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # SQL-Query, um alle Läden mit den Koordinaten und der Anzahl der Bewertungen zu holen
                cur.execute("""
                    SELECT s.store_id, s.latitude, s.longitude, COUNT(p.purchase_id) AS ratings_count
                    FROM stores s
                    LEFT JOIN purchases p ON s.store_id = p.store_id
                    GROUP BY s.store_id
                """)

                # Ergebnisse holen
                stores = cur.fetchall()

                # Ergebnisformat: Liste von Dictionaries mit lat, lng und der Anzahl der Bewertungen
                store_list = [
                    {"store_id": store[0], "latitude": store[1], "longitude": store[2], "ratings_count": store[3]}
                    for store in stores
                ]

                return store_list

    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

def coords_to_address(latitude, longitude):
    geolocator = Nominatim(user_agent="go2klo_app")
    location = geolocator.reverse((latitude, longitude))
    if location:
        return location.address
    else:
        return "Addresse nicht gefunden"