from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
import json

bookingAPI = Blueprint("booking api", __name__)

dbconfig = {
    
    'user':'abc',
    'database':'taipeiTrip',
    'password':'12345678',
    'auth_plugin':'mysql_native_password'
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 3,
                                                      **dbconfig)

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
#---------------------------------------------------------------------------------------------------------


@bookingAPI.route("/api/booking", methods=["GET"])
def getUndoneBookingInfo():
    return "HI"