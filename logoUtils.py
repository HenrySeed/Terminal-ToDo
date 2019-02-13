import datetime

def printLogo(win, x, y):
    logo = """ _____         _
|_   _|__   __| | ___
  | |/ _ \ / _` |/ _ \\
  | | (_) | (_| | (_) |
  |_|\___/ \__,_|\___/
"""
    stEndings = [1, 21, 31]
    rdEndings = [3, 23]

    dateNum = int(datetime.datetime.now().strftime('%d'))
    ending = "th"
    if dateNum in stEndings: ending = "st"
    if dateNum in rdEndings: ending = "rd"  

    date = datetime.datetime.now().strftime('%A - %d{0} %b %G'.format(ending))
    logo_lines = len(logo.split('\n'))

    win.addstr(y, x, logo)
    win.addstr(y+logo_lines, x, date)
