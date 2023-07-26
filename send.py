from tabnanny import filename_only
import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image
import json
from os import listdir
from os.path import join

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("Connected.")
        client.subscribe("Group_01/IMAGE/predict")
    else:
        print("Failed to connect, Error code: %d."% rc)

class_names = ['Ragdolls', 'Singapura', 'Persians', 'Sphynx', 'Scottish Folds']

def on_message(client,userdata,msg):
    print("Received message from server.")
    resp_dict=json.loads(msg.payload)
    print("Filename:%s, Prediction:%s"%(resp_dict["filename"], class_names[resp_dict["prediction"]]))

def setup(hostname):
    client=mqtt.Client()
    client.on_connect=on_connect
    client.on_message=on_message
    client.connect(hostname)
    client.loop_start()
    return client

def load_image(filename):
    img=Image.open(filename)
    img=img.resize((416,416))  # 修改为YOLOv7的输入尺寸
    imgarray=np.array(img)#/255.0
    #final=np.expand_dims(imgarray,axis=0)
    return imgarray

def send_image(client,filename):
    img=load_image(filename)
    img_list=img.tolist()
    file_name_only = filename.split('/')[-1]
    send_dict={"filename":file_name_only,"data":img_list}
    client.publish("Group_01/IMAGE/classify",json.dumps(send_dict))

def main():
    client = setup("172.25.101.161")
    PATH = "./input_images"
    for file in listdir(PATH):
        filename = join(PATH, file)
        print("Sending data for file: %s." % filename)
        send_image(client, filename)
        print("Done. Waiting for results")
    while True:
        pass

if __name__ == '__main__':
    main()
