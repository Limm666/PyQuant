# -*- coding:utf-8 -*- 
# author: limm_666
from configparser import ConfigParser
import mysql.connector

cp = ConfigParser()
cp.read("../config.conf")
mysql_host = cp.get("mysql", "db_host")
mysql_port = cp.get("mysql", "db_port")
mysql_user = cp.get("mysql", "db_user")
mysql_pwd = cp.get("mysql", "db_password")
mysql_database = cp.get("mysql", "db_database")

mydb = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user=mysql_user,
    passwd=mysql_database,
    database=mysql_database
)
print(mydb)
mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)
