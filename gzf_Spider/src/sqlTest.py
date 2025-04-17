
import mysql.connector
 
mydb = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="123456"   # 数据库密码
)

 
mycursor = mydb.cursor()
 
mycursor.execute("SHOW DATABASES")
 
for x in mycursor:
  print(x)
