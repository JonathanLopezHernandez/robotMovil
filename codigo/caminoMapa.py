import time
import os
import collections
import signal
import sys
import csv
from PIL import Image
from PIL import ImageDraw


matriz = []

with open('/home/pi/Desktop/matriz.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        matriz.append(row)
        


def bfs(matriz, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
##       print(path)
        x, y = path[-1]
        if matriz[y][x] == goal:
            return path
        for x2, y2 in ((x+10,y), (x-10,y), (x,y+10), (x,y-10)):
            if 0 <= x2 < width and 0 <= y2 < height and matriz[x2][y2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
                

wall= "9"
clear, goal = 1, 2
width, height = 512, 512

#matriz[270][170] = 2 #tngo que poner al reves la X y la Y
matriz[300][250] = 2 #tngo que poner al reves la X y la Y
path = bfs(matriz, (100, 300))
print(path)
img = Image.open("/home/pi/Desktop/mapa.png")
draw = ImageDraw.Draw(img)
img.show()
draw.line(path, width=1, fill="blue")
img.show()
#img.show()
img.save('/home/pi/Desktop/camino.png')

file = open("/home/pi/Desktop/camino.txt", "w")
file.write(str(path))
file.close()





