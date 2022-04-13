from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
from apiModel.apiModel import *
from settings.settings import PARTNER_KEY
import json
import requests

orderAPI = Blueprint("order api", __name__)

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
            "partner_key": PARTNER_KEY,
            "merchant_id": "leontien2008_CTBC",
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
            'x-api-key': PARTNER_KEY
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