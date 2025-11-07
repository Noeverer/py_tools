<<<<<<< HEAD
import mysql.connector
 
# 修改数据库连接参数，支持更多认证方式
mydb = mysql.connector.connect(
  host="127.0.0.1",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="Liu@06027",   # 数据库密码
  auth_plugin='mysql_native_password'  # 指定认证插件
=======

import mysql.connector
 
mydb = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="123456"   # 数据库密码
>>>>>>> c4ba579a8612b4f108b5dbfd52860c8932752113
)

 
mycursor = mydb.cursor()
 
mycursor.execute("SHOW DATABASES")
 
for x in mycursor:
<<<<<<< HEAD
  print(x)
=======
  print(x)
>>>>>>> c4ba579a8612b4f108b5dbfd52860c8932752113
