import RPi.GPIO as GPIO
import time
import os
import collections
import signal
import sys
import csv
from PIL import Image
from PIL import ImageDraw
from random import randint


pos = "n"
cuenta = 0
camino = '['
a = 110
c = 110
b = 290
d = 290
matriz = []

with open('/home/pi/Desktop/matriz.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        matriz.append(row)
        
# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Top
pinTrigger = 18
pinEcho = 24
# set GPIO left
pinTriggerL = 23
pinEchoL = 25
# set pin Motor
pinTop = 13
pinLeft = 6
pinRight = 19


def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup() 
	sys.exit(0)

signal.signal(signal.SIGINT, close)
GPIO.setwarnings(False)
# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)
GPIO.setup(pinTriggerL, GPIO.OUT)
GPIO.setup(pinEchoL, GPIO.IN)
##pin pa motor
GPIO.setup(pinTop, GPIO.OUT)
GPIO.setup(pinLeft, GPIO.OUT)
GPIO.setup(pinRight, GPIO.OUT)

def top():
    global b
    global a
    global camino
    global matriz
    global pos
    if(pos == "n"):
        b = b-10
        pos = "n"
    elif(pos == "s"):
        b = b-10
        pos = "s"
    elif(pos == "e"):
        a = a+10
        pos = "e"
    elif(pos == "o"):
        a = a-10
        pos = "o"
        camino = camino +'('+ str(a) + ', ' + str(b) + '),'
    
def rigth():
    global b
    global a
    global camino
    global matriz
    global pos
    if(pos == "n"):
        a = a+10
        pos = "e"
    elif(pos == "s"):
        a = a-10
        pos = "o"
    elif(pos == "e"):
        b = b+10
        pos = "s"
    elif(pos == "o"):
        b = b-10
        pos = "n"
    camino = camino +'('+ str(a) + ', ' + str(b) + '),'
    
def left():
    global b
    global a
    global camino
    global matriz
    global pos
    if(pos == "n"):
        a = a-10
        pos = "o"
    elif(pos == "s"):
        a = a+10
        pos = "e"
    elif(pos == "e"):
        b = b-10
        pos = "n"
    elif(pos == "o"):
        b = b+10
        pos = "s"
    camino = camino +'('+ str(a) + ', ' + str(b) + '),'

while cuenta < 1000:
    
    num = int(randint(0, 1) )
    if num < 1:
        print("Distcm")
    vuelta = 0
    GPIO.output(pinLeft, False)
    GPIO.output(pinTop, False)
    GPIO.output(pinRight, False)
    # set Trigger to HIGH
    GPIO.output(pinTrigger, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)

    startTime = time.time()
    stopTime = time.time()


    # save start time
    while 0 == GPIO.input(pinEcho):
        startTime = time.time()

    # save time of arrival
    while 1 == GPIO.input(pinEcho):
        stopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print ("DistanceTop: %.1f cm" % distance)

    GPIO.output(pinTriggerL, True)
    time.sleep(0.00001)
    GPIO.output(pinTriggerL, False)
	
    startTimeL = time.time()
    stopTimeL = time.time()
    # save start time
    while 0 == GPIO.input(pinEchoL):
        startTimeL = time.time()

    # save time of arrival
    while 1 == GPIO.input(pinEchoL):
        stopTimeL = time.time()

    # time difference between start and arrival
    TimeElapsedL = stopTimeL - startTimeL
    distanceL = (TimeElapsedL * 34300) / 2

    time.sleep(1)

    if(pos == "n"):
        d = b-10
    elif(pos == "s"):
        d = b-10
    elif(pos == "e"):
        c = a+10
    elif(pos == "o"):
        c = a-10
	
    if distance > 30 and matriz [c][d] != "1":
        top()
        GPIO.output(pinTop, 1)
        time.sleep(1)
        GPIO.output(pinTop, 0)
    else:
        num = int(randint(0, 1) )
        if num < 1 and matriz [c][d] != "1":
            left()
            GPIO.output(pinLeft, 1)
            time.sleep(1)
            GPIO.output(pinLeft, 0)
        else:
            rigth()
            GPIO.output(pinRight, 1)
            time.sleep(1)
            GPIO.output(pinRight, 0)            
    
    men = camino +']'
    mio  = eval(men)
    img = Image.open("/home/pi/Desktop/mapa.png")
    draw = ImageDraw.Draw(img)
    draw.line(camino, width=1, fill="blue")
    img.save('/home/pi/Desktop/caminoAleatorio.png')
    cuenta = cuenta + 1
    if cuenta >= 20:
            break

#path = bfs(matriz, (100, 300))
#print(path)
print(camino)
camino = camino +']'
mio  = eval(camino)
print(mio)
img = Image.open("/home/pi/Desktop/mapa.png")
draw = ImageDraw.Draw(img)
img.show()
draw.line(mio, width=1, fill="blue")
img.show()
#img.show()
img.save('/home/pi/Desktop/caminoAleatorio.png')

file = open("/home/pi/Desktop/caminoAleatorio.txt", "w")
file.write(str(camino))
file.close()





