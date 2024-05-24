import socket
from pymongo import MongoClient

def Main():
    db = dbConnect()

    host = '192.168.0.207'  # Server ip
    port = 8605

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mysocket.bind((host, port))
    print("Server Started")

    while True:
        data, addr = mysocket.recvfrom(1024)
        data = data.decode('utf-8')
        print(data)
        db.insert_one({"Detection" : data})
        print("Updata Database")

        objectDetails = db.find().sort("_id", -1).limit(10)
        for x in objectDetails:
            print(x['Detection'])


def dbConnect():
    try:
        conn = MongoClient(host="127.0.0.1", port=27017)
        print("Mongo Connected")
        return conn.HBD_Project.Detected_Objects_camera2
    except Exception as e:
        print("Error in Mongo Connection : ", e)

if __name__ == '__main__':
    Main()