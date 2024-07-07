import datetime
from os import getenv
from flask import Flask, request, jsonify
from models import todo
from bcrypt import hashpw, gensalt, checkpw
import jwt


us = todo.Users()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("JWT_SECRET_KEY")

@app.route("/")
def home():
    return jsonify({"message":"welcome to todo api",
                    "routes":{
                         "register": "/api/register",
                         "login": "/api/login" ,
                         "alltasks": "/api/todo" 
                        } })


# user creation route
@app.route("/api/register", methods = ["POST"])
def register():
    try:
        body = request.json
        if "username" not in body.keys() and "password" not in body.keys():
            return jsonify({"message":"username and password required!"}),400
        else:
            if len(body.keys()) > 2:
                return jsonify({ "message":"only 'username' and 'password' required!" }),400
            else:
                username = body["username"]
                password = str(body["password"])

                isuser = us.is_user(username)
                if isuser:
                    return jsonify({"message":"username already exist!"}),409
                else:
                    encoded_password = password.encode('utf-8')
                    salt = gensalt()
                    hashed_password = hashpw( password=encoded_password, salt=salt )
                    
                    user = { "username": username,"password":hashed_password }
                    us.register_user(document=user, app="todo")

                    return jsonify({"message":"user created successfully!"}),201

    
    except Exception as error:
        return jsonify({"server_error":f"{error}!"}),500



@app.route("/api/login", methods = ["POST"])
def login():
    try:
        body = request.json
        if "username" not in body.keys() and "password" not in body.keys():
            return jsonify({"message":"username and password required!"}),400
        else:
            if len(body.keys()) > 2:
                return jsonify({"message":"not more fields than username and password!"}),400
            else:
                username = body["username"]
                password = str(body["password"])

                user = us.find_user(username)
                if user:
                    password = password.encode('utf-8')
                    if checkpw(password, user["password"]):
                        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                        payload = {"username":f"{username}", "id":f"{user["_id"]}", "exp":expiration_time }
                        token = jwt.encode(payload,getenv("JWT_SECRET_KEY"),getenv("ALGORITHM"))

                        return jsonify({"message":"logged in successfully","token":f"{token}"}),200
                    else:
                        return jsonify({"message":"bad username or password!"}),401
                else:
                    return jsonify({"message":"bad username or password!"}),401


    except Exception as error:
        return jsonify({"server_error":f"{error}!"}),500



# error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":f"{error}"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"message":f"{error}"}), 405

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({"message":f"{error}"}), 415

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"message":f"{error}"}), 500



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=5003)