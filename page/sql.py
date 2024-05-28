from django.db import connection

def get_account():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM accounts")
        result = cursor.fetchall()
    return result