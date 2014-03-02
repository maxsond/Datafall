import collections	
import random

ab = map(chr, range(97, 123))
class col(list):

	def __init__(self,pos=0):
		list.__init__
		self.pos = pos	#The column index
		
	def update(self):
		self.insert(0,symbol(random.choice(ab)))
		
class symbol:
	
	def __init__(self,val=random.choice(ab),color="00CC00"):
		self.val = val + "\n"
		self.color = color
		
x = symbol()
print x.val
y = col()
y.update()
y.update()
y.update()
y.update()
for item in y:
	print item.val