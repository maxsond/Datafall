import time
import curses
import random
import sys
from winsize import x, y
x = x()
y = y()
win = curses.initscr()
curses.curs_set(0)
curses.start_color()
print curses.can_change_color()
curses.init_color(2, 256, 204, 0)
curses.init_pair(1, 2, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
win.border(0)
win.refresh()
colcount = 2

class player:
			
	def __init__(self,x=1,y=1,color=4,speed=0):
		self.x = x
		self.y = y
		self.color = color
		self.speed = speed
		self.ticks = 0
		self.body = "X"
		self.head = "*"
		
	def fall(self):
		self.speed = ticks + self.speed
		self.ticks = self.ticks + 1
	
	def stand(self,plat):
		self.speed = plat.speed
		
class plat:

	def __init__(self,val="_",x=1,y=1,color=3,speed=1):
		self.val = val
		self.x = x
		self.y = y
		self.color = color
		self.speed = speed
		
	def tick(self):
		self.y = self.y - self.speed

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

holybits = [(bob.y,bob.x),(firstplat.y,firstplat.x)]
		
def levelbits():

	global ind
	global outd
	global bob
	global firstplat
	global holybits
	
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
	
	bob.y = 2
	bob.x = 1
	win.addch(bob.y,bob.x,bob.body,curses.color_pair(4))
	win.addch(bob.y-1,bob.x,bob.head,curses.color_pair(4))
	win.refresh()
	holybits = [(bob.y,bob.x),(bob.y-1,bob.x),(firstplat.y,firstplat.x)]

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
		global colcount
		if len(self) <= self.winy-3:	#Fill the col
			y = 1
			x = self.pos
			self.update()
			#print self
			win.move(y,x)
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
			win.move(0,self.pos)
		else: 
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
			win.addch(c)
			win.refresh()
			time.sleep(self.speed)
#		except:
#			self.win.clear
#			curses.endwin()
#			print ""
#			print "Fatal error! Cursor went out of bounds!", self.x, self.y
		if wait:
			win.getch()
		win.border(0)
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