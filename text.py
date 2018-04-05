# -*- coding: utf-8 
import psycopg2
conn = psycopg2.connect(database="msi", user="postgres",password="123456", host="172.16.0.53",port="5433")
print ("connect successful")
cursor = conn.cursor()
	# 这里是数据库查询语句????
tool = "螺丝刀"
cursor.execute("SELECT roomid,goodlocation FROM goods WHERE goodsname= %s ;",(tool,))
rows = cursor.fetchall()
for i in rows:
    print (i[0])
print (rows[0])
