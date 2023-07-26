# wsl-yolov7-catdetect
record prof colin's baseline-cat detect
use yolov7 to train five different cats-classes=["persian","ragdoll","scottish","singpura","sphynx"]
in order to enhance pre, use imagenet to pretrain, and then use our own dataset.

# 1.collect data

every one search 200+ images of one single species, and use YoloLabel_v1.2.1 to annotate(draw a frame of one or many cats of the same species in one picture)
the tool is very easy to use just search YoloLabel_v1.2.1
after annotating images we collect about 1000 images in total

# 2.make dataset

as my own computer's cpu is not good enough and I met such many bugs when using gpu in my local computer, use colab's free gpu instead.
upload the dataset directory to colab.
the directory needs to be set as :

![image](https://github.com/SCUcookie/wsl-yolov7-catdetect/assets/103986681/fcb0a18a-e75b-4d7b-97aa-e3d8c32726b2)

train valid data.yaml
train and valid directory need to have images directory which contains images and lables directory which contains the lables of every images.

![image](https://github.com/SCUcookie/wsl-yolov7-catdetect/assets/103986681/c5ba6b90-b118-428d-9981-9caf92db9be8)

# 3.train

when upload cloud directory in colab, run

`%cd /content/drive/MyDrive/YOLOv5-Lite`

`!pip install -r requirements.txt`

which makes sure colab pip yolo's requrements

then

`python train.py --weights yolov7.pt --data dataset_sampe/data.yaml --workers 4 --batch-size 4 --img 416 --cfg cfg/training/yolov7.yaml --name yolov7 --hyp data/hyp.scratch.p5.yaml --epochs 25`

which can adjust our own parameters

if use gpu add `--device 0`

# remember to modify data.yaml, just change the route where your dataset locates #

when finishing we will get results in 'train' directory and get 'best.pt' in its weight directory.

# 4.moquitto

then I modify the 'detectcb.py' to call the model

if we want to use model in Raspberry Pi, we need use mosquitto to transport message, its camera takes photos using 'send.py' to transport it to my 'receive.py', attention send.py should be run in the computer which also running vncserver which control the robot.

run 'receive.py' before running 'send.py'

all we have to modify is the ip address, also we have to use the same wifi.

# 5.deploy model

when we correctly run the two python file, we can detect every pictures the robot taken to every species the picture belongs to in real time.
