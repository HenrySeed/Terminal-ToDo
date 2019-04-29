from logoUtils import print_logo
import os
from cursesUtils import *
import math


def get_line_split(inputLineStr, max_width):
    """
        Takes a line and returns it split into an array with each item being a line of the right length
    """
    
    # check for a long inputLineStr
    text = inputLineStr.replace('[ ] ', "")
    lines = []
    
    currentLine = ""
    for word in text.split(' '):
        if len(currentLine + " " + word) < max_width:
            currentLine += word + " "
        else:
            # check if a word is longer than the max width by itself
            if currentLine == "":
                while len(word) > max_width:
                    lines.append(word[:max_width])
                    word = word[max_width:]
                if word != "":
                    lines.append(word)
            else:
                lines.append(currentLine)
                currentLine = word + " "

    if currentLine != "":
        lines.append(currentLine)
    return lines


def get_split_newTodo(todo):
    """
        Returns the new todo field, split so the new lines wrap
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    # 10 is the length of the left margin and the " new Todo"
    max_width = int(columns) - 10
    return get_line_split(todo, max_width)


def get_split_todo(todo):
    """
        Returns the given todo, split so the new lines wrap
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    # 7 is the length of the left margin and the "[ ] "
    max_width = int(columns) - 7
    return get_line_split(todo, max_width)


def is_todo_multiLine(inputLineStr):
    """
        Returns True | False based on if the given string will occupy more than one line on the todo
    """
    if len(get_split_todo(inputLineStr)) > 1:
        return True
    else:
        return False


def print_todo_line(win, y, x, inputLineStr, checked, done):
    """
        Prints a given todo item
    """

    lines = get_split_todo(inputLineStr)

    # win.addstr(25, 0, " " * 400)
    # win.addstr(25, 0, str(lines))

    if done:
        text_color = curses.color_pair(2)
        tick_color = curses.color_pair(2)
        tick = "[x]"
    else:
        text_color = curses.color_pair(3)
        tick_color = curses.color_pair(3)
        tick = "[ ]"


    count = 0
    for line in lines:
        if count == 0:
            win.addstr(y+count, x, tick, tick_color)

        win.addstr(y+count, x+5, line, text_color)

        count += 1

    # re return the number of lines so we can move the next one down
    return count


def print_new_todo_input(win, todo, tbCursor, active, linesUsed):
    """
        Prints the new todo input to the curses window with the cursor.
    """
    str_lines = get_split_newTodo(todo)

    count = 1
    for line in str_lines:
        if count == 1:
            win.addstr(linesUsed+count, 0, "New TODO: " + line)
        else:
            win.addstr(linesUsed+count, 0, "          " + line)
        count += 1

    return linesUsed + count
 


def print_todo(win, listTodo, doneList, cursorLine, linesUsed):
    """
        Prints the todoList and the doneList to the curses window
    """
    listX = 3
    listY = linesUsed+1

    win.addstr(listY, 0, " TODO ------------------")
    # the y screen position of the start of the list

    listY += 1
    itemCount = 0
    count = 0
    for todo in listTodo:
        count += print_todo_line(win, listY+count, listX, todo, cursorLine == itemCount, False)
        itemCount += 1

    win.addstr(listY+count+1, 0, " DONE ------------------")
    # the y screen position of the start of the list
    listY += 2
    for todo in doneList:
        count += print_todo_line(win, listY+count, listX, todo, cursorLine == itemCount, True)
        itemCount += 1




def updateCursor(win, cursorPos, tbCursor, newTodo, todoList, doneList, start):
    """
        janky cursor move system. Needs to be updated to use win.move(y, x)
    """
    # if its in the text field
    if cursorPos == -1:
        # get the string before the cursor so we can find the lines
        pre_cursor = newTodo[0:tbCursor]
        # get the newTodo lines
        str_lines = get_split_newTodo(pre_cursor)
        # get the y (number of lines), x (len of last line)
        y, x = len(str_lines), len(str_lines[-1])

        win.addstr(start-1, 10+x-1, "")
    else:
        found_line = False
        lineCount = start + 2
        index = 0

        for item in todoList:
            if index == cursorPos:
                win.addstr(lineCount, 4, "")
                found_line = True
                break
            else:
                lineCount += len(get_split_todo(item))
            index += 1

        # add the break between the lists
        lineCount += 2

        if not found_line:
            for item in doneList:
                if index == cursorPos:
                    win.addstr(lineCount, 4, "")
                    found_line = True
                    break
                else:
                    lineCount += len(get_split_todo(item))
                index += 1



def printHelp(win):
    height,width = win.getmaxyx()
    leftMargin = math.floor(width / 2 - 17)

    if width > 35:
        win.addstr(height-1, leftMargin + 0, "esc/q:      enter:      del:", curses.color_pair(4))
        win.addstr(height-1, leftMargin + 6, "quit")
        win.addstr(height-1, leftMargin + 18, "done")
        win.addstr(height-1, leftMargin + 28, "delete")

    # win.addstr(height-2, 0, "esc: quit  enter: Done  backspace: Delete")


def print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo, logo, noDate, noHelp):
    """
        Prints all three UI elements to the curses window, logo, new todo Input and the todo list
    """
    linesUsed = print_logo(win, 0,0, logo, noDate)
    linesUsed = print_new_todo_input(win, newTodo, tbCursor, textField, linesUsed)
    print_todo(win, todoList, doneList, cursorPos, linesUsed)

    if noHelp == "False":
        printHelp(win)

    updateCursor(win, cursorPos, tbCursor, newTodo, todoList, doneList, linesUsed)

