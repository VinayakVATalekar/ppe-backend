
from pymongo import MongoClient
import datetime
import random


client = MongoClient()
	

list=["sagar","pritam","ajay","jagdish","rahul","gulshan","anshuman","chetan","ujwal","vikram"]
dec=["hand glove","boot","helmet","vest"]

db = client['my_db']

mycollection = db['camera']
#number of records wanto enter 
t=15
isodate =datetime.datetime.now()

for i in range(1,t):
	db['camera'].insert_one( { "cam_id": i,
     "Camera_Name": f"cmaera {i}",
     "Location": f"section {i}",
     "Date_and_Time": isodate,
     "is_working": True,
     "is_paused": False
    }  
	
 )
#no of alert msgs to enter 	
al=20			
for j in range(1,al):
	r=random.randrange(0,9)
	d=random.randrange(0,4)
	db['alert'].insert_one(
                {
     "msg_id" : f"{100+j}",
     "Camera_Name": f"camera {j}",
     "Location": f"section {j}",
     "Date_and_Time": isodate,
     "Detection_Type":dec[d],
     "Employee_Name": list[r],
     "Reference_Number": f"{1000+j}",
     "Annotated_Image": "url_link [for image resource]",
     "Details": [
     {
     "id": 1,
     "text": "detail 1"
     },
     {
     "id": 2,
     "text": "detail 2"
     }
     ]
    }
    ) 

