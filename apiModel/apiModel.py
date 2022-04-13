import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
import sys
sys.path.append('../')
from settings.settings import USER, PASSWORD

#----------------------------------------------------------------
# print(USER, PASSWORD)

dbconfig = {  
    'user':USER,
    'database':'taipeiTrip',
    'password':PASSWORD,
    'auth_plugin':'mysql_native_password'
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 10,
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
#----------------------------------------------------------------
def getID(id):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions where id = %s")
    data_query=(id, )
    cursor.execute(query, data_query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results

#a = getID(6)
#print(a)



def getResults(pages):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions order by id limit 12 offset %s")
    data_query=(pages, )
    cursor.execute(query, data_query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results



def getKeywords(keyword, pages):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions where attractions.name like %s limit 12 offset %s")
    data_query=('%'+ keyword +'%', pages)
    cursor.execute(query, data_query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results

def db_getInfoByID(id):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions WHERE id = %s")
    data_query=(id, )
    cursor.execute(query, data_query)
    data = cursor.fetchone()
    cursor.close()
    cnx.close()
    if data:
        return data

# a = db_getInfoByID(2)
# print(a)

def db_getUserIdBySession(name):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT member.id FROM member WHERE member.name = %s")
    data_query=(name,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        return user

def db_getBookingInfoByUserId(id):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor(buffered=True)
    query = ("SELECT * FROM booking WHERE booking.user_id = %s order by ordertime DESC")
    data_query=(id,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        return user

# a = db_getBookingInfoByUserId(3)
# print(a)

def db_getAttractionDataById(id):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions WHERE id = %s")
    data_query=(id,)
    cursor.execute(query, data_query)
    data = cursor.fetchone()
    cursor.close()
    cnx.close()
    if data:
        return data

def db_deleteBookingById(id):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    sql = "DELETE FROM booking WHERE booking.user_id = %s"
    data_sql = (id, )
    cursor.execute(sql, data_sql)
    cnx.commit()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!deleteDone!!!!!!!!!!!!!!!!!!!!!!!!")
    cursor.close()
    cnx.close()

#db_deleteBookingById(2)


def db_getUserIdBySession(name):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT member.id FROM member WHERE member.name = %s")
    data_query=(name,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        return user


def db_getOrderIdByUserId(id):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor(buffered=True)
    query = ("SELECT * FROM orders WHERE orders.user_id = %s order by ordertime DESC")
    data_query=(id,)
    cursor.execute(query, data_query)
    orderData = cursor.fetchone()
    cursor.close()
    cnx.close()
    if orderData:
        return orderData

# a = db_getOrderIdByUserId(1)[0]
# print(a)

def db_changeStatus(orderId):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("UPDATE orders SET order_status=0 WHERE id= %s")
    data_query=(orderId,)
    cursor.execute(query, data_query)
    cnx.commit()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!changeDone!!!!!!!!!!!!!!!!!!!!!!!!")
    cursor.close()
    cnx.close()

#db_changeStatus(2)

def db_deleteBookingById(id):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    sql = "DELETE FROM booking WHERE booking.user_id = %s"
    data_sql = (id, )
    cursor.execute(sql, data_sql)
    cnx.commit()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!deleteDone!!!!!!!!!!!!!!!!!!!!!!!!")
    cursor.close()
    cnx.close()