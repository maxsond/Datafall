import display
import threading
import sys
import winsize
import time
import random
x = winsize.x()
y = winsize.y()

class myThread(threading.Thread):

	def __init__(self,threadID,type,col):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.type = type
		self.col = col
	def run(self):
		self.col.dis()
		
matrix = []
for i in range(1,x-1):
	matrix.append(myThread(i,i,display.col(i)))

while matrix != []:
	i = random.choice(matrix)
	i.start()
	matrix.pop(matrix.index(i))
	
	time.sleep(0.1)