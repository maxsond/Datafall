import time
import curses
import random
import sys
from winsize import x, y
#import manager
import threadz
notdead = True
x = x()
y = y()
winx = x
winy = y
win = curses.initscr()
curses.curs_set(0)
curses.start_color()
print curses.can_change_color()
curses.init_color(2, 256, 204, 0)
curses.init_pair(1, 2, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
curses.init_pair(5,curses.COLOR_RED,curses.COLOR_BLACK)
win.border(0)
win.refresh()
colcount = 2
curses.noecho()
holybits = []
platlist = []
#win.addstr(curses.keyname(262))

def restart():
	notdead = False
	win.clear()
	levelbits()

def death():
	global notdead
	notdead = False
	msg(y/2,x/2,speed=0.1,txt="YOU DIED",align='center').tw(False)
	time.sleep(1)
	sys.exit()

def intro():
	msg(y/2,x/2,speed=0.1,txt="Press Space",align='center').tw(False)
	time.sleep(0.5)
	msg(y/2,x/2,speed=0.1,txt="           ",align='center').tw(False)
	
def ootime():
	global notdead
	notdead = False
	msg(y/2,x/2,speed=0.1,txt="TOO SLOW",align='center').tw(False)
	time.sleep(1)
	sys.exit()
	
class player:
			
	def __init__(self,x=1,y=1,color=4,speed=0):
		self.x = x
		self.y = y
		self.color = curses.color_pair(color)
		self.speed = speed
		self.ticks = 0
		self.body = "X"
		self.head = "*"
		self.standing = True
		self.loc = (y,x)
		
	def fall(self):				
		#Speed should be added to self.Y in order to go up, 
		#so it should typically be a negative number when standing on a platform
		#And positive when falling
		try:
			win.addch(self.y,self.x,' ',curses.color_pair(3))
			win.addch(self.y-1,self.x,' ',curses.color_pair(4))
			self.y = self.y + self.speed
		except:
			pass
		try:
			win.addch(self.y,self.x,self.body,curses.color_pair(3))
			win.addch(self.y-1,self.x,self.head,curses.color_pair(4))
			self.speed = self.speed + self.ticks
			self.ticks = self.ticks + 1
		except:
			death()
			#sys.exit()
	
	def stand(self,platform):
		if self.speed + platform.speed > 15:
			death()
		else:
			self.speed = -(platform.speed)
			
	def move(self):
		global platlist
		if self.x < x-2:
			self.x += 1
			self.loc = (self.y,self.x)
			try:
				win.addch(self.y,self.x,self.body,curses.color_pair(4))
				win.addch(self.y-1,self.x,self.head,curses.color_pair(4))
				win.addch(self.y,self.x-1,' ')
				win.addch(self.y-1,self.x-1,' ')
				win.addch(2,1,'_')
				win.refresh()
			except:
				pass
		else:
			pass
		win.addstr(winy-2,7,str(platlist))
		win.addstr(winy-4,7,str((self.y,self.x)))
		if self.loc in platlist:
			self.standing = True
			win.addstr(winy-3,7,"True")	
			bobplatindex = platlist.index(self.loc)
			bobplat = platcases[bobplatindex]
			self.stand(bobplat)
		else:
			win.addstr(winy-3,7,"False")
			#win.addstr(winy-4,7,"False")
			self.standing = False
			self.fall()
			pass
		#win.addstr(0,0,str((self.y,self.x)))
		#self.tick()
	'''		
	def tick(self):
		if self.standing == True:
			self.stand(platcases[)
		else:
			self.fall()
	'''
	
class plat:

	def __init__(self,x=1,y=1,speed=1,val="_",color=3):
		self.val = val
		self.x = x
		self.y = y
		self.lasty = y
		self.color = color
		self.speed = speed
		#holybits.append((y,x))
		
	def tick(self):
		'''This returns the plat to the bottom of the screen'''
		if self.y <= 2:
			self.lasty = self.y
			try:
				win.addch(self.y,self.x," ")
			except:
				pass
			self.y = winy - self.y
			#holybits.append((self.y,self.x))
		'''This moves the plat one (speed) up'''
		if self.y >= winy - 2:
			self.lasty = self.y
			try:
				win.addch(self.y,self.x," ")
			except:
				pass
			self.y -= self.speed
			#holybits.append((self.y,self.x))
		else:
			win.addch(self.y,self.x," ")
			'''
			try:
				win.addch(self.y,self.x,"_",curses.color_pair(3))
				win.addch(self.y+self.speed,self.x," ")
			except:
				pass
			'''
			#win.addch(self.y,self.x,"_",curses.color_pair(3))
			self.lasty = self.y
			win.addch(self.y,self.x," ")
			self.y = self.y - self.speed
			#holybits.append((self.y,self.x))
			#win.refresh()

class indoor:	#Coordinates are for the upper half of the door

	def __init__(self,y=0,x=1):
		self.x = x
		self.y = y
		self.upperhalf = "/"
		self.lowerhalf = "\\"

class outdoor:	#Coordinates are for the upper half of the door
		
	def __init__(self,y=0,x=0):
		self.x = x
		self.y = y
		self.upperhalf = "\\"
		self.lowerhalf = "/"

		
ind = indoor()
outd = outdoor()
bob = player()
firstplat = plat()
lastplat = plat()
platcases = []

#holybits = [(bob.y,bob.x),(firstplat.y,firstplat.x)]
testplats = []	
def levelbits():

	global ind
	global outd
	global bob
	global firstplat
	global lastplat
	global testplats
	global platcases
	#global holybits
	
	for i in range(2,5):
		testplats.append(plat(i,2,0))
	for i in testplats:
		win.addch(i.y,i.x,"_")
	for i in testplats:
		platlist.append((int(i.y),int(i.x)))
		platcases.append(i)
	bouncyplat = plat(8,6,10)
	platcases.append(bouncyplat)
	platlist.append((bouncyplat.y,bouncyplat.x))
	win.addch(bouncyplat.y,bouncyplat.x,"_")
			
		
	
	ind.x = 0
	ind.y = 1
	win.addch(ind.y,ind.x,ind.upperhalf)
	win.addch(ind.y+1,ind.x,ind.lowerhalf)
	
	firstplat.x = 1
	firstplat.y = 2
	
	outd.x = x-1
	outd.y = random.randrange(1,y-3)
	win.addch(outd.y,outd.x,outd.upperhalf)
	win.addch(outd.y+1,outd.x,outd.lowerhalf)
	
	lastplat.x = x - 2
	lastplat.y = outd.y + 1
	win.addch(lastplat.y,lastplat.x,'_')
	
	bob.y = 2
	bob.x = 1
	win.addch(bob.y,bob.x,bob.body,curses.color_pair(3)) #Should be pair 3 when standing still, 4 when falling
	win.addch(bob.y-1,bob.x,bob.head,curses.color_pair(3))
	win.refresh()
	#holybits = [(bob.y,bob.x),(bob.y-1,bob.x),(firstplat.y,firstplat.x)]
	platlist.append((firstplat.y,firstplat.x))
ab = map(chr, range(97, 123))
class col(list):

	def __init__(self,pos=1,winx = x,winy = y):
		list.__init__
		self.pos = pos	#The column index
		self.winx = winx
		self.winy = winy
		self.full = False
		
	def update(self):
		self.insert(0,symbol(random.choice(ab)))
	
	def filtick(self):
	#	manager.tick()
	
		global colcount
		if len(self) <= self.winy-3:	#Fill the col
			y = 1
			x = self.pos
			self.update()
			#print self
			win.move(y,x)
			for i in self:
				win.addstr(y,x,self[self.index(i)].val,curses.color_pair(1))
				try:
					y += 1
					win.move(y,x)
				except:
					pass
			win.move(0,self.pos)
		else:
			if self in threadz.o.cols:
				pass
			else:
				threadz.o.cols.append(self)
			self.full = True
			self.insert(0,self.pop())	#Rotate by 1
			y = 1
			x = self.pos
			for i in self:
				if ((y,x) in holybits):
					pass
				else:
					win.addstr(y,x,self[self.index(i)].val,curses.color_pair(1))
				try:
					y += 1
					win.move(y,x)
				except:
					pass
					

class symbol:
	
	def __init__(self,val=random.choice(ab),color=1):
		self.val = val
		self.color = color
		
	def color(self):
		if random.randrange(1,5) == 1:
			self.color = 2
		else:
			self.color = 1


class msg:
	
	def __init__(self,y=0,x=0,speed=0.1,txt="Test String",align='right'):
		self.txt = txt
		self.x = x + 1
		self.y = y + 1
		self.speed = speed
		self.align = align
		
	def al(self, align):	#Represents how the text should be horizontally aligned relative to (x,y)
		if align == 'right':
			return self.x
		elif align == 'center':
			return self.x - len(self.txt)/2
		elif align == 'left':
			return self.x - len(self.txt)

	def tw(self,wait):
		"""Taps out a message like a typewriter.

		msg -> Message to be tapped out
		w -> Window to work in
		x,y -> Where the cursor should start
		"""
		#try:
		win.move(self.y,self.al(self.align))
		for c in self.txt:
			h = win.getyx()[0]
			i = win.getyx()[1]
			#holybits.append((h,i))
			win.addch(c,curses.color_pair(5))
			win.refresh()
			time.sleep(self.speed)
			win.move(h,i+1)
#		except:
#			self.win.clear
#			curses.endwin()
#			print ""
#			print "Fatal error! Cursor went out of bounds!", self.x, self.y
		if wait:
			win.getch()
		#win.border(0)
		win.refresh()
def end():
	win.erase()
	win.refresh()
	curses.endwin()
def clear():
	win.erase()
	win.border(0)
	win.move(1,1)
	win.refresh()
def inp(msg):
	win = curses.initscr()
	try:
		msg.tw(False)
		#print msg.y+1, msg.al('right')
		return win.getstr(msg.y+1,msg.x)
		#print win.is_wintouched()
		#print xyz.is_wintouched()
		win.refresh()
	except:
		exit()
def test():
	time.sleep(0.5)
def tick():
	win.addstr(1,1,str(bob.standing))
	if notdead:
		for i in threadz.plats:
			try:
				win.addch(i.y,i.x,"_")
				win.addch(i.y+i.speed,i.x," ")
			except:
				try:
					win.addch(i.lasty,i.x," ")
				except:
					pass
		win.border(0)
		win.addch(lastplat.y,lastplat.x,'_')
		win.addch(firstplat.y,firstplat.x,'_')
		win.addch(ind.y,ind.x,ind.upperhalf)
		win.addch(ind.y+1,ind.x,ind.lowerhalf)
		win.addch(outd.y+1,outd.x,outd.lowerhalf)
		win.addch(outd.y,outd.x,outd.upperhalf)
		try:
			win.addch(bob.y,bob.x,bob.body)
			win.addch(bob.y-1,bob.x,bob.head)
		except:
			pass #Maybe put die call in here?
		win.addch(ind.y,ind.x,ind.upperhalf)
		win.refresh()
