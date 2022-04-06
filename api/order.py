from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
import json
import requests

orderAPI = Blueprint("order api", __name__)

dbconfig = {
    
    'user':'abc',
    'database':'taipeiTrip',
    'password':'12345678',
    'auth_plugin':'mysql_native_password'
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 10,
                                                      **dbconfig)


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
#------------------------------------------------------------------------------





@orderAPI.route("/api/order", methods=["POST"])
def createNewOrder():
    req = request.get_json()
    print("#########################",req,"################################")
    if "name" in session:
        userID = db_getUserIdBySession(session['name'])[0]
        attractionID=req['order']['trip']['attraction']['id']
        address=req['order']['trip']['attraction']['address']
        image=req['order']['trip']['attraction']['image']
        date=req['order']['trip']['date']
        time=req['order']['trip']['time']
        price=req['order']['price']
        order_name=req['order']['contact']['name']
        order_email=req['order']['contact']['email']
        order_phone=req['order']['contact']['phone']
        order_status= 1 # 1: 代表還沒付款 / 0： 代表付款成功

        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        add_order = ("INSERT INTO orders"
            "(user_id, attraction_id, address, image, date, time, price, order_name, order_email, order_phone, order_status)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")
        data_value = (userID, attractionID, address, image, date, time, price, order_name, order_email, order_phone, order_status)
        cursor.execute(add_order, data_value)
        cnx.commit()
        print('closing')
        cursor.close()
        cnx.close()

        #後端發prime/partner_key...等資料給tappay
        tappay_url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        prime = {
            "prime": req['prime'],
            "partner_key": 'partner_Dt4FMiBYyoQ94pyucVyV50XLrqlgG6V3TzY055AuzbnMa3k1v7lzdZ3O',
            "merchant_id": "leontien2022_CTBC",
            "details":"TapPay TaipeiTrip Test",
            "amount": price,
            "cardholder": {
                "phone_number": order_phone,
                "name": order_name,
                "email": order_email,
            },
            "remember": False
        }
        header = {
            'Content-Type': 'application/json',
            'x-api-key': 'partner_Dt4FMiBYyoQ94pyucVyV50XLrqlgG6V3TzY055AuzbnMa3k1v7lzdZ3O'
        }       
        body = json.dumps(prime)

        req = requests.post(tappay_url, data=body, headers=header)
        userPayResult = req.json()
        print(userPayResult)

        if userPayResult['status'] == 0:
            orderID = db_getOrderIdByUserId(userID)[0]
            db_changeStatus(orderID)
            db_deleteBookingById(userID)
            return {
                'data':{
                    'number':orderID,
                    'payment':{
                        'status':0,
                        'message':'付款成功'
                    }
                }
            }

        else:{
            'data':{
                    'number':orderID,
                    'payment':{
                        'status':1,
                        'message':'付款失敗'
                    }
                }
            }
    else:
        return {'error':True, 'message':'系統錯誤'}


@orderAPI.route("/api/order/<number>")
def fetchOrderInfo(number):
    if "name" in session:
        userID = db_getUserIdBySession(session['name'])[0]
        orderID = db_getOrderIdByUserId(userID)[0]
        print(orderID)
        return {'orderID':orderID}