from flask import *
import mysql.connector
from mysql.connector import errorcode

# 跟資料庫要資料
cnx = mysql.connector.connect(user='abc',
                              database='taipeiTrip',
                              password='12345678',
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

def db_query(email, password):
    query = ("SELECT * FROM member WHERE member.email = %s AND member.password = %s")
    data_query=(email, password)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    data = {}
    data['data'] = {}
    if user:
        data['data']['id'] = user[0]
        data['data']['name'] = user[1]
        data['data']['email'] = user[2]
        return data
    else:
        return "no data"
# a = db_query('test@test.com', 'test123')
# print(a)

userAPI = Blueprint("user api", __name__)
@userAPI.route("/api/user", methods=["GET", "POST"])
def getUserInfo():
    return "hi"
