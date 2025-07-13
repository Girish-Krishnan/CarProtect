import os
import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv('credentials.env')

def get_connection():
    """Create and return a new MySQL connection using env variables."""
    return mysql.connect(
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DATABASE'],
        user=os.environ['MYSQL_USER'],
        passwd=os.environ['MYSQL_PASSWORD']
    )
