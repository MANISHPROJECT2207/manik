import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Mee1074$'
)

cursorObject = dataBase.cursor()

cursorObject.execute("create database manik;")

# cursorObject.execute("drop database manik;")

print("Ho Gaya!")