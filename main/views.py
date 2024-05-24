import glob
import os
import threading
#from concurrent.futures import ThreadPoolExecutor

from django.http import JsonResponse,HttpResponse
import cv2
import gridfs
import pymongo
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.decorators import gzip
from .models import *

import cv2
import socket
import pickle
import numpy as np

@gzip.gzip_page
def index(request):
    files = glob.glob('mediafiles/videos/*')
    for f in files:
        os.remove(f)
    
    context = videoList()
    return render(request, "main/home.html", context)


@gzip.gzip_page
def LiveCam1(request):
    try:
        cam1_url = "rtsp://cs2projs:cs2projs@192.168.0.10/stream1"
        cam = VideoCamera(cam1_url)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

    return render(request, 'main/liveCam1.html')


@gzip.gzip_page
def LiveCam2(request):
    try:
        cam2_url = "rtsp://cs2admin:cs2projs@192.168.0.148/stream1"
        camera = VideoCamera(cam2_url)
        return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

    return render(request, 'main/liveCam2.html')

@gzip.gzip_page
def garbagechute(request):
    return render(request, "main/garbagechute.html")

@gzip.gzip_page
def sample(request):
    return render(request, "main/sample.html")

@gzip.gzip_page
def evidence(request):
    return render(request, "main/evidence.html")


# Video Capture
class VideoCamera(object):
    def __init__(self, camera_name):
        self.video = cv2.VideoCapture(camera_name)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n' + frame)


def videoList():
    dbname = dbConnect()
    fs = gridfs.GridFS(dbname)
    data = dbname.fs.files.find().sort("uploadDate", -1).limit(5)
    video_names = []
    detection = []
    detection_details=[]

    detail = dbname.Detected_Objects
    objectDetails = detail.find().sort("_id", -1)
 
    for video in data: #modify
        fs_id = (video['_id'])
        video_name = f"{video['filename']}"
        video_names.append(video_name)
        output_data = fs.get(fs_id).read()
        filename = f"mediafiles/videos/{video['filename']}"
        output = open(filename, "wb")  # write bytes
        output.write(output_data)
        output.close()
        print(f"{video['filename']} download Complete") 

        for x in objectDetails:
            details_data = x['Detection']
            if isinstance(details_data, dict) and 'Id' in details_data and details_data['Id'] == video_name:
                 # details_data is a dictionary and contains the key 'Id'
                detection.append(details_data['Metadata']['Detections']['ObjectSubType'])
                detection_details.append(details_data)  # 
                break 
   
            elif isinstance(details_data, str):# details_data is a string  
                #details_word = x['Detection']
                details_words = details_data.split()
                last_details_word = f"{details_words[-1]}.mp4"
                if last_details_word==f"{video['filename']}":
                    first_word= details_words[0]
                    detection.append(first_word)
                    detection_details.append(None)
                    break
    context = {"video_names": video_names, "Video": Video.objects.all(), "garbage": detection, "detection_details":detection_details}
    return (context)


def listpage(request):
    context = videoList()
    return render(request, "main/videoList.html", context)


def deleteList(request):
    delete_video_name = request.GET.get('video')
    {"delete_video_name": delete_video_name}

    if request.method == "POST":
        dbname = dbConnect()
        fs = gridfs.GridFS(dbname)
        delete_video_name = request.GET.get("video")
        data = dbname.fs.files.find_one({"filename": delete_video_name})
        fs_id = (data['_id'])
        fs.delete(fs_id)
        return redirect('/')

    context = {"delete_video_name": delete_video_name}
    return render(request, "main/delete.html", context)


def dbConnect():
    try:
        conn = pymongo.MongoClient(host="127.0.0.1", port=27017)
        print("Mongo Connected")
        return conn.HBD_Project
    except Exception as e:
        print("Error in Mongo Connection : ", e)

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip1 = "192.168.0.207"
port1 = 8500
s1.bind((ip1, port1))
def live1():
    
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ip = "192.168.0.207"
    # port = 8500
    # s.bind((ip, port))
    while True:
        x = s1.recvfrom(1000000)
        #clientip = x[1][0]
        data = x[0]

        data = pickle.loads(data)

        imo = cv2.imdecode(data, cv2.IMREAD_COLOR)
        frame = cv2.imencode('.jpg', imo)[1].tobytes()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame)

def video_feed1(request):
    return StreamingHttpResponse(live1(), content_type="multipart/x-mixed-replace;boundary=frame")

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip2 = "192.168.0.207"
port2 = 8600
s2.bind((ip2, port2))
def live2():
    
    while True:
        x = s2.recvfrom(1000000)
        #clientip = x[1][0]
        data = x[0]

        data = pickle.loads(data)

        imo = cv2.imdecode(data, cv2.IMREAD_COLOR)
        frame = cv2.imencode('.jpg', imo)[1].tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame)

def video_feed2(request):
    return StreamingHttpResponse(live2(), content_type="multipart/x-mixed-replace;boundary=frame")

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip3 = "192.168.0.207"
port3 = 8700
s3.bind((ip3, port3))
def live3():
    
    while True:
        x = s3.recvfrom(1000000)
        #clientip = x[1][0]
        data = x[0]

        data = pickle.loads(data)

        imo = cv2.imdecode(data, cv2.IMREAD_COLOR)
        frame = cv2.imencode('.jpg', imo)[1].tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame)

def video_feed3(request):
    return StreamingHttpResponse(live3(), content_type="multipart/x-mixed-replace;boundary=frame")
    

def update_detection(request):
    detection = ""
    db = dbConnect().Detected_Objects
    objectDetails = db.find().sort("_id", -1).limit(10)
    for x in objectDetails:
        detection += f"{x['Detection']} \n"
        print(x['Detection'])

    return JsonResponse({"detection":detection})

def update_detection1(request):
    detection = ""
    db = dbConnect().Detected_Objects_camera2
    objectDetails = db.find().sort("_id", -1).limit(5)
    for x in objectDetails:
        detection += f"{x['Detection']} \n"
        print(x['Detection'])

    return JsonResponse({"detection":detection})




#{"detection":"Hasitha Karunathilaka"}
