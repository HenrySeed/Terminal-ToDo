import datetime

def print_logo(win, x, y, CustomLogo, nodate):
  """
    Prints the logo to the curses window. Can accept a custom logo and a date boolean to hide the date.
  """
  
  logo = """ _____            _
|_   _|__      __| | ___
  | |/ _ \ __ / _` |/ _ \\
  | | (_) |__| (_| | (_) |
  |_|\\___/    \\__,_|\\___/
"""
  # If we have a valid custom logo
  if len(CustomLogo) > 0 and CustomLogo != " ":
    logo = "\n" + CustomLogo
    logo_lines = len(logo.split('\n'))
  # If we have a space logo (means bo logo)
  elif CustomLogo == " ":
    logo = ""
    logo_lines = 0
  # if we have n o custom logo, just use the default one
  else:
    logo_lines = len(logo.split('\n')) - 1
  
  # PRint eh given logo to the curses window
  win.addstr(y, x, logo)

  # generate the date
  if nodate == "False":\
      # get the current date number eg: 13
      dateNum = int(datetime.datetime.now().strftime('%d'))

      # endings for dates eg 13th or 22nd ot 21st
      stEndings = [1, 21, 31]
      rdEndings = [3, 23]
      ending = "th"
      if dateNum in stEndings: ending = "st"
      if dateNum in rdEndings: ending = "rd"  

      # generate the date string eg: Thursday - 14th Feb 2019
      date = datetime.datetime.now().strftime('%A - %d{0} %b %G'.format(ending))

      # print to the curses window
      win.addstr(y+logo_lines+1, x, date)

      # return the line we finished on plus some padding for the new todo input which comes next
      return y + logo_lines+2

  else:
    # if we havent used a date we use less padding for the new todo input which comes next
    return y + logo_lines

     
