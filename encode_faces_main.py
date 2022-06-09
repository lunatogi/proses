#!/usr/bin/env python3

# USAGE
# When encoding on laptop, desktop, or GPU (slower, more accurate):
# python3 encode_faces_main.py --dataset dataset --encodings encodings.json --cascade haarcascade_frontalface_default.xml --detection-method cnn
# When encoding on Raspberry Pi (faster, more accurate):
# python3 encode_faces_main.py --dataset dataset --encodings encodings.json --cascade haarcascade_frontalface_default.xml --detection-method hog

# import the necessary packages
from imutils import paths
import face_recognition
import gui as gui
#import mxnet as mx
import argparse
import pickle
import numpy as np
import json
import cv2
import os
import shutil
import time

def EncodeProccess(name, surname, tc, job, comp, code):
    workerName = name
    print(workerName)
    print("Eğer isim kısmına sadece 'q' yazarsanız işlem bitirilir")
    print("İsminizi girdikten sonra ilk fotoğrafı çekmeye hazırlanın...")
    #workerName = input("İsminizi girin : ")
    #if workerName == "q":
        #break
    os.makedirs('./dataset/'+workerName)
    os.system('raspistill -w 320 -h 240 -o ./dataset/'+workerName+'/0000.jpg')
    print("İkinci fotoğraf için hazırlanın...")
    gui.ChangeInfo("İkinci fotoğraf için hazırlanın...")
    time.sleep(3)
    os.system('raspistill -w 320 -h 240 -o ./dataset/'+workerName+'/0001.jpg')

    personNum = ""
    with open("number.json", "r") as read_file:
        data = json.load(read_file)
        personNum = str(data["number"])
    dirName = personNum + ".json"

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", required=False,
        help = "path to where the face cascade resides")
    ap.add_argument("-i", "--dataset", required=False,
        help="path to input directory of faces + images")
    ap.add_argument("-e", "--encodings", required=False,
        help="path to serialized db of facial encodings")
    ap.add_argument("-d", "--detection-method", type=str, default="hog",
        help="face detection model to use: either `hog` or `cnn`")
    args = vars(ap.parse_args())

    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images("dataset"))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model='hog')

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    knownEncodings1 = np.array(knownEncodings).tolist()
    knownNames1 = np.array(knownNames).tolist()

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings1, "names": knownNames1, "surname": surname, "tc": tc, "job": job, "comp": comp, "code": code}
#    f = open(args["encodings"], "w",  encoding="utf8")
    with open(dirName, "w") as a:
        json.dump(data,a)
#    f.close()

    passint = (int(personNum)+1)
    personNum = str(passint)
    numberUpdate = {"number" : personNum}
    with open("number.json", "w") as n:
        json.dump(numberUpdate,n)

    d = './dataset'
    shutil.rmtree(d)
