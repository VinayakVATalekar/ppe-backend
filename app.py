from flask import Flask
from flask import jsonify
from flask import request
import mongo 

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
user=[]
password=[]


@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    up={}  
    use=mongo.check_user(username) 
    if use is False:
         up["username"]=username
         up['password']=password
         mongo.add_user(up)
         return jsonify({'msg':"user succsesfully registered"})  
    return {"msg":"username already exists"} 
     

@app.route("/users", methods=["GET"])
##()

def get_all_users():
    data=[]
    userr=mongo.get_allusers()
    for x in userr:
        x["_id"]=str(["_id"])
        data.append(x)

    return jsonify(data), 200

#user login method

@app.route("/login",methods=["POST"])
def login():
    useName=request.json.get("username",None)
    pword=request.json.get("password",None)
    fun=mongo.get_user(useName)
    if fun is None:
        return {"msg:":"wrong username "}
    if fun["password"]==pword:
        acc_token=create_access_token(identity=useName)
        return jsonify(acc_token=acc_token)
    return {"msg":"wrong password"}

@app.route("/logout",methods=["POST"])
#()
def logout():
    
    userid=get_jwt_identity()
    print(userid)

@app.route("/camera", methods=["POST"])
#
def addcamera():
    camera = request.json
    if camera is None:
        return {"message":"No Request found"}
    mongo.add_camera(camera)
    return {"message":"Camera successfully added"}
    

@app.route("/alert", methods=["POST"])
#
def sumation():
    msg = request.json
    if msg is None:
        return {"message": "No request found"}
    mongo.add_alert(msg)
    return {"message":"msg successfully added"}




@app.route("/cameras",methods=["GET"])
#
def cameras():
    data=[]
    cam_list= mongo.GET_all_camera()
    for doc in cam_list:
        doc['_id'] = str(doc['_id']) # This does the trick!
        data.append(doc)
    return jsonify(data)
    
 
@app.route("/camera/id",methods=["GET"])
#
def camera_id():
    doc=[]
    #geting cam_id
    camid=request.json
    id= mongo.get_camera(camid)
    id['_id']=str(id['_id'])
    doc.append(id)
    return jsonify(doc)


@app.route("/alerts",methods=["GET"])
#
def alerts():
    al=mongo.GET_all_alert()
    art=[]
    for x in al:
        x['_id']=str(x['_id'])
        art.append(x)
    return jsonify(art)       
    
@app.route("/alert/msg_id",methods=["GET"])
#
def alert_msg():
    al=request.json
    mg=[]
    msg=mongo.get_alert(al)
    msg['_id']=str(msg['_id'])
    mg.append(msg)
    return jsonify(mg)

@app.route("/alert_pg",methods=["GET"])
#
def get_page():
    page=request.json.get("page_no",None)
    entry=request.json.get("entry_no",None)
    pn=mongo.pagination(entry,page)
    data=[]
    for x in pn:
        x["_id"]=str(x["_id"])
        data.append(x)
    return jsonify(data)    




if __name__ == "__main__":
    app.run(debug=True)