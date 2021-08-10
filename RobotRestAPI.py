import RPi.GPIO as GPIO
import time
import flask
import json
from flask import request

app = flask.Flask(__name__)

# global current degree variable
currDegree = 0

# GPIO set up and start
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
servo1 = GPIO.PWM(11, 50)
servo1.start(0)
print("Waiting 2 seconds after starting.")
time.sleep(2)

@app.route('/rotate', methods=['POST'])
def rotate():
    global currDegree
    currDegree = int(request.get_json()['degree'])
    print("Changing to requested degree: ", currDegree)
    servo1.ChangeDutyCycle(currDegree/18 + 2)
    time.sleep(.7)
    servo1.ChangeDutyCycle(0)
    time.sleep(.3)
    return json.dumps({'degree':currDegree})
    
if __name__ == '__main__':
    app.run(host = '192.168.0.138', port = 5000)