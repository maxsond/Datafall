import display
import threading
import sys
import winsize
import time
import random
#	import manager	
x = winsize.x()
winx = x
y = winsize.y()
winy = y
fullcols = -1
newm = []
matrix = []
plats = []	#List of display.plat objects
platthreads = []

class myThread(threading.Thread):
	s = float(random.randrange(1,5)) / 10.0
	def __init__(self,threadID,type,col,speed = s):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.type = type
		self.col = col
		self.speed = speed
	def run(self):
		while display.notdead:
			self.col.filtick()
			#display.win.refresh()
			time.sleep(2.7) #The time between each tick
		return None

	
class colCounter(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.cols = []
		
	def run(self):
		while display.notdead == True:
			if len(self.cols) >= len(newm):
				display.ootime()
		return None

class streamer(threading.Thread):
	def __init__(self,threadID="streamer"):
		threading.Thread.__init__(self)
		self.threadID=threadID
		
	def run(self):
		global matrix
		global newm
		while matrix != []:
			i = random.choice(matrix)
			i.start()
			newm.append(matrix.pop(matrix.index(i)))
	#		colCounter.start()
			time.sleep(0.9)
			
class platthread(threading.Thread):
	def __init__(self,index=0,threadID="plats"):
		threading.Thread.__init__(self)
		self.threadID=threadID
		self.index = index
		
	def run(self):
		while display.notdead:
				plats[self.index].tick()
				time.sleep(1)
		return None

class updater(threading.Thread):
	def __init__(self,index=0,threadID="updater"):
		threading.Thread.__init__(self)
		self.threadID=threadID
		self.index = index
	
	def run(self):
		while display.notdead:
			display.tick()
			time.sleep(0.1)
		return None
o = colCounter()
			
def init():
	global o
	xpick = []
	for i in range(1,x-1):
		matrix.append(myThread(i,i,display.col(i)))
	a = streamer()
	a.start()
	#halfcols = (winx - 2)/2
	#for i in range(len(matrix)):
		#plats.append(display.plat(winsize.y()-1,random.randint(2,winsize.x() - 2),random.randint(1,3)))
	for i in range(2,winx - 2):
		xpick.append(i)
	while xpick != []:
			#c = random.randint(2,winx - 2)
			#c = random.
		c = random.choice(xpick)
		platinstance = display.plat(xpick.pop(xpick.index(c)),(winy - 4),random.randint(1,3))
		plats.append(platinstance)
		display.platlist.append((platinstance.y,platinstance.x))
		display.platcases.append(platinstance)
	for p in plats:
		#plats is a list of display.plat objects
		#plat is a threadz object
		q = platthread(plats.index(p))
		q.start()
		platthreads.append(q)
	u = updater()
	u.start()
	o.start()
	
def end():
	display.notdead = False