from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling

# 跟資料庫要資料
# cnx = mysql.connector.connect(user='abc',
#                               database='taipeiTrip',
#                               password='12345678',
#                               auth_plugin='mysql_native_password')
# cursor = cnx.cursor()

#----------------------------------------------------------------
dbconfig = {

    'user':'abc',
    'database':'taipeiTrip',
    'password':'12345678',
    'auth_plugin':'mysql_native_password'
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 3,
                                                      **dbconfig)
#-----------------------------------------------------------------
#每次檢查要資料
def db_getUserInfo(name):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.name = %s")
    data_query=(name,)
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
# a = db_query('test@test.com', 'test123')
# print(a)
def db_memberSignin(email, password):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.email = %s AND member.password = %s")
    data_query=(email, password)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        #print(user)
        return user
#註冊
def db_checkEmail(email):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.email = %s")
    data_query=(email, )
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        #print(user)
        return user
#db_checkEmail("ply@ply.com")

def db_addNewMember(name, email, password):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    add_member = ("INSERT INTO member "
                  "(name, email, password) " 
                  "VALUES (%s, %s, %s)")
    data_member = (name, email, password)
    cursor.execute(add_member, data_member)
    cnx.commit()
    #print("add success")
    cursor.close()
    cnx.close()

#-----------------------------------------------------------------
userAPI = Blueprint("user api", __name__)


@userAPI.route("/api/user", methods=["GET"])
def checkUserStatus():
    if "name" in session:
        data = db_getUserInfo(session['name'])
        return data
    return {"data": None}


@userAPI.route("/api/user", methods=["POST"])
def signup():
    #name = request.form["name"]
    #email = request.form["email"]
    #print(email)
    #password = request.form["password"]
    req = request.get_json()
    user = db_checkEmail(req['email'])
    #print(user)
    if user:
        return {
                "error": True,
                "message":"信箱已經被註冊"
        }      
    else:
        db_addNewMember(req['name'], req['email'], req['password'])
        return {"ok":True}

@userAPI.route("/api/user", methods=["PATCH"])
def signin():
    req = request.get_json()
    member = db_memberSignin(req['email'], req['password'])
    if member:
        session['name'] = member[1]
        return {"ok":True}
    else:
        return {"error": True, "message": "信箱或密碼錯誤"}
    

@userAPI.route("/api/user", methods=["DELETE"])
def signout():
    session.pop('name', None)
    return {"ok":True}