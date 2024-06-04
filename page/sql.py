from django.db import connection
from .models import *
class Account:
    def getData(platform):
        return AccountDB.objects.filter(platform=platform)
    def getData():
        return AccountDB.objects.all()
    def modifyData(where, data):
        AccountDB.objects.filter(platform=where).update(account=data)
    def deleteData(platform):
        AccountDB.objects.filter(platform=platform).delete()
    def deleteDataAll():
        AccountDB.objects.all().update('connected', False)
    def addData(platform, account):
        AccountDB.objects.create(platform=platform, account=account)
    def getConnectedAccount():
        return AccountDB.objects.filter(connected=True)

class Content:
    def getData():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM page_contentdb")
            result = cursor.fetchall()
        return result
    def modifyData(where, data):
        ContentDB.objects.filter(platform=where).update(text=data)
    def deleteData(platform):
        ContentDB.objects.filter(platform=platform).delete()
    def deleteDataAll():
        ContentDB.objects.all().delete()
    def addData(platform, text):
        ContentDB.objects.create(platform=platform, text=text)

    
def get_account():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM page_accountdb")
        result = cursor.fetchall()
    return result

def del_account():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM page_accountdb")
        result = cursor.fetchall()
    return result

def add_account(platform, account):
    AccountDB.objects.create(platform='Facebook', account='temp')

def modify_account(platform, account):
    AccountDB.objects.filter(platform='Facebook').update(account='temp')