from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
from apiModel.apiModel import *
import json

bookingAPI = Blueprint("booking api", __name__)

@bookingAPI.route("/api/booking", methods=["GET"])
def getBookingInfo():
    if "name" in session:
        print(session['name'])
    
        userID = db_getUserIdBySession(session['name'])[0]
        print(userID)
        result = db_getBookingInfoByUserId(userID)

        print(result)
        if result == None:
            return {"data":"noData"}
        attractionData = db_getAttractionDataById(result[2])
        preBooking={"data":""}
        preBooking['data']={
            "attraction":{
                "id": result[2],
                "name":attractionData[1],
                "address":result[3],
                "image":result[4]
            },
            'date':result[5],
            'time':result[6],
            'price':result[8]
        }

        print(preBooking)
        return preBooking

        
    return {"error": True, "message":"something went wrong"}


@bookingAPI.route("/api/booking", methods=["POST"])
def createNewBookingInfo():
    req = request.get_json()
    #print(req)
    if "name" in session:
            userID = db_getUserIdBySession(session['name'])[0]
            attractionID = req['attractionId']
            data = db_getAttractionDataById(attractionID)
            address = data[4]
            image = json.loads(data[9])[0]
            date = req['date']
            time = req['time']
            price = req['price']
            print("#1",userID,"#2",attractionID,"#3", address,"#4", image,"#5", date,"#6", time,"#7", price)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()
            add_booking = ("INSERT INTO booking"
                "(user_id, attraction_id, address, image, date, time, price)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s) ")
            data_value = (userID, attractionID, address, image, date, time, price)
            cursor.execute(add_booking, data_value)
            cnx.commit()
            print('closing')
            cursor.close()
            cnx.close()
            return {"ok":True}
    else:
        return {"error":"something is worong"}



@bookingAPI.route("/api/booking", methods=["DELETE"])
def deleteBooking():
    if "name" in session:
        userID = db_getUserIdBySession(session['name'])[0]
        print("####################",userID,"####################")
        db_deleteBookingById(userID)
        return {"ok":True}
    return {"error":True, "message": "User Not Login"}
