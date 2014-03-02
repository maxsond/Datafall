import curses

win = curses.initscr()
def main(win):
	curses.start_color()
	curses.use_default_colors()
	curses.init_color(curses.COLOR_GREEN, 797, 0, 0)
	curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
	win.addstr(str(curses.can_change_color()), curses.color_pair(1))
	win.refresh()

curses.wrapper(main)