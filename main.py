import display
import threadz
import curses
import time
import sys
import os
#y = symbol()
#print type(y.val)
def main():
	display.levelbits()
	display.intro()
	#threadz.init()
	
	while True:
		if display.win.getch() == ord(' '):
			#try:
			display.bob.move()
			#display.holybits[0] = (display.bob.y,display.bob.x)
			#display.holybits[1] = (display.bob.y-1,display.bob.x)
			display.win.refresh()
			#except:
			#	pass
		elif (display.win.getch() == ord('q') or display.win.getch() == ord('Q')):
			threadz.end()
			display.msg(display.y/2,display.x/2,speed=0.1,txt="Shutting Down...",align='center').tw(False)
			time.sleep(0.5)
			curses.endwin()
			os.system('cls' if os.name == 'nt' else 'clear')
			sys.exit()
		display.tick()
		time.sleep(0.1)
if __name__ == "__main__":
	main()