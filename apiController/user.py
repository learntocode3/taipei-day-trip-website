from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
from apiModel.apiModel import *

userAPI = Blueprint("user api", __name__)

@userAPI.route("/api/user", methods=["GET"])
def checkUserStatus():
    if "name" in session:
        data = db_getUserInfo(session['name'])
        print(data)
        print(session['name'])
        if data:
            return data
        return {"data": None}
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