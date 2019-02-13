import curses


def setupColour(win):
    # Uses default terminal colours
    curses.use_default_colors()
    curses.init_pair(0, 0, -1)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
