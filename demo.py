from flask import Flask,jsonify,request
from flask_cors import CORS

import bcrypt
import mongo 

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity,get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  
jwt = JWTManager(app)


def hashing(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return (hash)
    
@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    up={}  
    use=mongo.check_user(username) 
    if use is False:
         up["username"]=username
         has=hashing(password)
         up['password']=has
         mongo.add_user(up)
         return jsonify({'msg':"user succsesfully registered"})  
    return {"msg":"username already exists"} 
     

@app.route("/users", methods=["GET"])
@jwt_required()

def get_all_users():
    data=[]
    userr=mongo.get_allusers()
    for x in userr:
        x["_id"]=str(["_id"])
        data.append(x)

    return jsonify(data), 200



@app.route("/login",methods=["POST"])
def login():
    useName=request.json.get("username",None)
    pword=request.json.get("password",None)
    fun=mongo.get_user(useName)
    if fun is None:
        return {"msg:":"wrong username "}
    bytes = pword.encode('utf-8')
    res=bcrypt.checkpw(bytes,fun["password"])
    if res is True:
        acc_token=create_access_token(identity=useName)
        return jsonify(acc_token=acc_token)
    return {"msg":"wrong password"}

from blocklist import BLOCKLIST

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )

@app.route("/logout", methods=["POST"])

@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"message": "Successfully logged out"}, 200


@app.route("/camera", methods=["POST"])
@jwt_required()
def addcamera():
    camera = request.json
    if camera is None:
        return {"message":"No Request found"}
    mongo.add_camera(camera)
    return {"message":"Camera successfully added"}
    

@app.route("/alert", methods=["POST"])
@jwt_required()
def sumation():
    msg = request.json
    if msg is None:
        return {"message": "No request found"}
    mongo.add_alert(msg)
    return {"message":"msg successfully added"}


@app.route("/cameras",methods=["GET"])
@jwt_required()
def cameras():
    data=[]
    cam_list= mongo.GET_all_camera()
    for doc in cam_list:
        doc['_id'] = str(doc['_id']) 
        data.append(doc)
    return jsonify(data)
    
 
@app.route("/camera/id",methods=["GET"])
@jwt_required()
def camera_id():
    doc=[]
    camid=request.json
    id= mongo.get_camera(camid)
    id['_id']=str(id['_id'])
    doc.append(id)
    return jsonify(doc)


@app.route("/alerts",methods=["GET"])
@jwt_required()
def alerts():
    al=mongo.GET_all_alert()
    art=[]
    for x in al:
        x['_id']=str(x['_id'])
        art.append(x)
    return jsonify(art)       
    
@app.route("/alert/msg_id",methods=["GET"])
@jwt_required()
def alert_msg():
    al=request.json
    mg=[]
    msg=mongo.get_alert(al)
    msg['_id']=str(msg['_id'])
    mg.append(msg)
    return jsonify(mg)

@app.route("/page",methods=["GET"])
@jwt_required()
def get_page():
    page=request.json.get("page_no",None)
    entry=request.json.get("entry_no",None)
    pn=mongo.pagination(entry,page)
    data=[]
    
    data.append(dict)
    for x in pn:
        x["_id"]=str(x["_id"])
        data.append(x)
    dict={"entry_no":entry,"page_no":page,"pagination":data}    
    return jsonify(dict)    




if __name__ == "__main__":
    app.run( debug = True)
