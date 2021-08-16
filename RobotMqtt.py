from decimal import Decimal
import RPi.GPIO as GPIO
import math
import requests
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import threading

# global variables
currDegree = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
servo1 = GPIO.PWM(11, 50)



myMQTTClient = AWSIoTMQTTClient("YuriID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a3ipvdebeiblku-ats.iot.us-east-2.amazonaws.com", 8883)

myMQTTClient.configureCredentials("/home/pi/RobotArm/AWSCertificates/AmazonRootCA1.pem",
                                  "/home/pi/RobotArm/AWSCertificates/RP_private.pem.key",
                                  "/home/pi/RobotArm/AWSCertificates/RP_certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
print ('Initiating Realtime Data Transfer From Raspberry Pi...')
myMQTTClient.connect()

def rotate(self, params, packet):
    global currDegree
    currDegree = int(json.loads(packet.payload.decode('UTF-8'))['degree'])
    print("setPosition: " + str(currDegree))
    time.sleep(1)
    servo1.ChangeDutyCycle(currDegree/18 + 2)
    time.sleep(.7)
    servo1.ChangeDutyCycle(0)
    time.sleep(.3)

def setup():
    # GPIO set up and start
    servo1.start(0)
    print("Waiting 2 seconds after starting.")
    time.sleep(2)
    myMQTTClient.subscribe("motor/rotate", 1, rotate)

def reportPosition():
    while True:
        time.sleep(5)
        try:
            myMQTTClient.publish(
                topic="motor/position",
                QoS=1,
                payload='{"degree":" ' + str(currDegree)+'"}')
            print("reportPosition: " + str(currDegree))
        except Exception as e:
            print(e.message)

if __name__ == '__main__':
    setup()
    reportPosition()