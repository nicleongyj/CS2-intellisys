import json
from pymongo import MongoClient
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("CS2/GarbageDetection")  # subscribe topic

def on_message(client, userdata, msg):
    data = msg.payload.decode('utf-8')
    data_dict = json.loads(data)
    #print(data)
    db = dbConnect()  
    db.insert_one({"Detection": data_dict})
    print("Updated Database")

    objectDetails = db.find().sort("_id", -1).limit(10)
    for x in objectDetails:
        print(x['Detection'])

def dbConnect():
    try:
        conn = MongoClient(host="127.0.0.1", port=27017)
        print("MongoDB Connected")
        return conn.HBD_Project.Detected_Objects
    except Exception as e:
        print("Error in MongoDB Connection: ", e)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("192.168.0.207", 1883, 60)
    except Exception as e:
        print("Error connecting to MQTT Broker: ", e)
        return

   
    client.loop_forever()

if __name__ == '__main__':
    main()
