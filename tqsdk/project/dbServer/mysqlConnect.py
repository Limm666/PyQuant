# -*- coding:utf-8 -*- 
# author: limm_666

import mysql.connector

mydb = mysql.connector.connect(
    host="**.**.**",
    user="***",
    passwd="***",
    database="***"
)
print(mydb)
mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)
