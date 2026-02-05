import os
import django
from django.db import connections
from django.db.utils import OperationalError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_forum.settings')
django.setup()

def check_database():
    db_conn = connections['default']
    try:
        db_conn.cursor().execute('SELECT 1;')
        print("Database connection successful!")
    except OperationalError as e:
        print("Database connection failed:")
        print(e)

if __name__ == "__main__":
    check_database()