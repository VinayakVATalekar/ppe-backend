import pymongo


client = pymongo.MongoClient()
db = "my_db"

def add_user(user_password):
    client['my_db']['username'].insert_one(user_password)


def get_user(useName):
    return client['my_db']['username'].find_one({"username":useName})

def check_user(username):
   if  client['my_db']['username'].find_one({"username":username}):
       return True
   return False


def get_camera(cam_id):
   return client["my_db"]["camera"].find_one(cam_id)


def add_camera(camera):
    client["my_db"]["camera"].insert_one(camera)


def get_alert(msg_id):
    return client["my_db"]["alert"].find_one(msg_id)

   
def add_alert(msg):
    client["my_db"]["alert"].insert_one(msg)
    

def GET_all_camera():
    return client["my_db"]["camera"].find()


def GET_all_alert():
    return client["my_db"]["alert"].find().sort("Date_and_Time",-1)

def pagination(entry,page):
    cur_st=(page-1)*entry
    cur_end=cur_st+entry
    cursur=client["my_db"]['alert'].find().sort("Date_and_Time",-1)
    return cursur[cur_st:cur_end]

    