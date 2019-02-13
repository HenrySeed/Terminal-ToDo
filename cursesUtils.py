import curses

def setupColour(win):
    """
        Sets colors to be used in curses
    """
    # Uses default terminal colours
    curses.use_default_colors()
    curses.init_pair(0, 0, -1)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
