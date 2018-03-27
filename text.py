import psycopg2
conn = psycopg2.connect(database="msi", user="postgres",password="123456", host="172.16.0.63",port="5433")
print "connect success"