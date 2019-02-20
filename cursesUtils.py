import curses



CURSOR_X = 0
CURSOR_Y = 0


def cursorMove(y, x):
    CURSOR_X = x
    CURSOR_Y = y


def get_x_y():
    return [CURSOR_X, CURSOR_Y]


def setupColour(win):
    """
        Sets colors to be used in curses
    """
    # Uses default terminal colours
    curses.use_default_colors()
    curses.init_pair(0, 0, -1)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)


