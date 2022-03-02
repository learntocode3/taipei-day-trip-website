from flask import Blueprint
from flask import *
import mysql.connector
from mysql.connector import errorcode
import json

attractions = Blueprint('attractionApi', __name__)


def getID(id):
    cnx = mysql.connector.connect(user='root',
                                  password='12345678',
                                  database="taipeiTrip",
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions where id = %s")
    data_query=(id, )
    cursor.execute(query, data_query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results



def getResults(pages):
    cnx = mysql.connector.connect(user='root',
                                  password='12345678',
                                  database="taipeiTrip",
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions order by id limit 12 offset %s")
    data_query=(pages, )
    cursor.execute(query, data_query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results



def getKeywords(keyword, pages):
    cnx = mysql.connector.connect(user='root',
                                  password='12345678',
                                  database="taipeiTrip",
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM attractions where attractions.name like %s limit 12 offset %s")
    data_query=('%'+ keyword +'%', pages)
    cursor.execute(query, data_query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results



@attractions.route("/api/attraction/<attractionId>")
def getDataById(attractionId):
    try:
        results = getID(attractionId)
        if results:
            attraction = []
            for ele in results:
                new_data = {}
                new_data['id'] = ele[0]
                new_data['name'] = ele[1]
                new_data['category'] = ele[2]
                new_data['description'] = ele[3]
                new_data['address'] = ele[4]
                new_data['transport'] = ele[5]
                new_data['mrt'] = ele[6]
                new_data['latitude'] = ele[7]
                new_data['longtitude'] = ele[8]
                new_data['images'] = json.loads(ele[9])
                attraction.append(new_data)
            data = {"data":attraction}
            return jsonify(data)
        else:
            return {"error":True, "message": "景點編號不正確"}, 400
    except:

        return {"error" : True, "message" : "伺服器內部錯誤"}, 500
    






@attractions.route("/api/attractions")
def getAttractions():
    try:
        page = request.args.get('page','0')
        page = int(page)       
        keyword = request.args.get('keyword','')
        # 設定nextpage跟offset
        nextPage = page + 1
        pages = 12 * page
        
        # 如果沒有keyword
        if keyword == "":
            results = getResults(pages)
            attractionList = []
            for ele in results:
                new_data = {}
                new_data['id'] = ele[0]
                new_data['name'] = ele[1]
                new_data['category'] = ele[2]
                new_data['description'] = ele[3]
                new_data['address'] = ele[4]
                new_data['transport'] = ele[5]
                new_data['mrt'] = ele[6]
                new_data['latitude'] = ele[7]
                new_data['longtitude'] = ele[8]
                new_data['images'] = json.loads(ele[9])
                attractionList.append(new_data)
            
            data = {"nextPage" : nextPage,
                    "data" : attractionList}

            if len(results) == 0:
                data['nextPage'] = None
                data['data'] = None

            return jsonify(data)
        else:
            results = getKeywords(keyword, pages)
            attractionList = []
            for ele in results:
                new_data = {}
                new_data['id'] = ele[0]
                new_data['name'] = ele[1]
                new_data['category'] = ele[2]
                new_data['description'] = ele[3]
                new_data['address'] = ele[4]
                new_data['transport'] = ele[5]
                new_data['mrt'] = ele[6]
                new_data['latitude'] = ele[7]
                new_data['longtitude'] = ele[8]
                new_data['images'] = json.loads(ele[9])
                attractionList.append(new_data)
            

            data = {"nextPage" : nextPage,
                    "data" : attractionList}

            if len(results) == 0:
                data['nextPage'] = None
                data['data'] = None


            return jsonify(data)

        


    
    
    except:
        return {"error" : True, "message" : "伺服器內部錯誤"}, 500
        