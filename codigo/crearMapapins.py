import RPi.GPIO as GPIO
import time
import signal
import sys
import os
import csv
import collections
from PIL import Image
from PIL import ImageDraw

matriz = []
for i in range(512):
    matriz.append([0]*512)

for i in range(512):
    for j in range(512):
        matriz[i][j]=9

matriz [a][b] = 1
matriz [a][b+10] = 1
mensaje = mensaje +'('+ str(a) + ', ' + str(b) + '),'

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
    global mensaje
    global matriz
    if(matriz[a][b+10] == 1):
        b = b-10
    elif(matriz[a][b-10] == 1):
        b = b+10
    elif(matriz[a+10][b] == 1):
        a = a-10
    elif(matriz[a-10][b] == 1):
        a = a+10
    matriz [a][b] = 1
    mensaje = mensaje +'('+ str(a) + ', ' + str(b) + '),'
    
def rigth():
    global b
    global a
    global mensaje
    global matriz
    if(matriz[a][b+10] == 1):
        a = a+10
    elif(matriz[a-10][b] == 1):
        b = b+10
    elif(matriz[a+10][b] == 1):
        b = b-10
    elif(matriz[a][b-10] == 1):
        a = a-10
    matriz [a][b] = 1
    mensaje = mensaje +'('+ str(a) + ', ' + str(b) + '),'
    
def left():
    global b
    global a
    global mensaje
    global matriz
    if(matriz[a-10][b] == 1):
        b = b-10
    elif(matriz[a][b+10] == 1):
        a = a-10
    elif(matriz[a+10][b] == 1):
        b = b+10
    elif(matriz[a][b-10] == 1):
        a = a+10
    matriz [a][b] = 1
    mensaje = mensaje +'('+ str(a) + ', ' + str(b) + '),'

while cuenta < 1000:
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
    # calculate distance
    distance = (TimeElapsed * 34300) / 2

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
	
    if distanceL < 30:
        if distance > 30:
            top()
            GPIO.output(pinTop, 1)
            time.sleep(1)
            GPIO.output(pinTop, 0)
        else:
            rigth()
            GPIO.output(pinRight, 1)
            time.sleep(1)
            GPIO.output(pinRight, 0)            
    else:
        left()
        GPIO.output(pinLeft, 1)
        time.sleep(1)
        GPIO.output(pinLeft, 0)
        
    cuenta = cuenta + 1
    if cuenta >= 20:
            break

mensaje = mensaje +']'
mio  = eval(mensaje)
print (mio)
dotSize = 2
draw.line(matriz, width=dotSize, fill="red")
img.save('/home/pi/Desktop/mapa.png')


with open('/home/pi/Desktop/matriz.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(matriz)



            
