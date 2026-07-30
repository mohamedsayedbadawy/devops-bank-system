"""
db.py
Responsible for connecting to MySQL and returning a database connection.
Connection settings are read from environment variables so the same code
works locally and later inside Docker Compose.
"""

import os
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.environ["DB_PORT"]),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
}


def get_connection():
    """
    Returns a new MySQL database connection.
    Raises mysql.connector.Error if the connection cannot be established.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        # Let the caller (app.py) decide how to respond to the client;
        # here we just make sure the failure is visible in the logs.
        print(f"[db.py] Database connection failed: {e}")
        raise
