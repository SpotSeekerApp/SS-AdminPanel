"""Flask configuration."""

FLASK_ENV = 'development'
TESTING = True
SECRET_KEY = "KPC4LKd7KvF0nRPGpvmv3Q"
STATIC_FOLDER = 'static'
TEMPLATES_FOLDER = 'templates'

USERNAME = 'postgres'
PASSWD = '12345'
HOST = 'localhost'
DB_PORT = '5432'
DBNAME = 'spotseeker'
DSN = f"""user='{USERNAME}' password='{PASSWD}' host='{HOST}' port='{DB_PORT}' dbname='{DBNAME}'"""

WEB_PORT = "8080"
localhost_ip = "127.0.0.1"
tmp_dir = "tmp"