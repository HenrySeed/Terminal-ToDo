from logoUtils import print_logo
import os
from cursesUtils import *


def get_line_split(inputLineStr):
    """
        Takes a line and returns it split into an array with each item being a line of the right length
    """
    rows, columns = os.popen('stty size', 'r').read().split()

    # check for a long inputLineStr
    text = inputLineStr.replace('[ ] ', "").strip()
    lines = []
    # 7 is the length of the left margin and the "[ ] "
    max_width = int(columns) - 7

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


def is_todo_multiLine(inputLineStr):
    """
        Returns True | False based on if the given string will occupy more than one line on the todo
    """
    if len(get_line_split(inputLineStr)) > 1:
        return True
    else:
        return False



def print_todo_line(win, y, x, inputLineStr, checked, done):
    """
        Prints a given todo item
    """

    lines = get_line_split(inputLineStr)
    
    count = 0
    for line in lines:
        if count == 0:
            if checked:
                win.addstr(y+count, x, "[ ] " + line)
            elif done:
                win.addstr(y+count, x, "[x] " + line)
            else:
                win.addstr(y+count, x, "[ ] " + line)
        else:
            win.addstr(y+count, x, "    " + line)

        count += 1

    # re return the number of lines so we can move the next one down
    return count


def print_new_todo_input(win, todo, tbCursor, active, linesUsed):
    """
        Prints the new todo input to the curses window with the cursor.
    """
    todoString = todo
    win.addstr(linesUsed+1,0, "New TODO: " + todoString)
    # if active:
    #     win.addstr(linesUsed+1,10 + tbCursor, "█")


def print_todo(win, listTodo, doneList, cursorLine, linesUsed):
    """
        Prints the todoList and the doneList to the curses window
    """
    listX = 3
    listY = linesUsed+3

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




def updateCursor(win, cursorPos, tbCursor, todoList, doneList, start):
    """
        janky cursor move system. Needs to be updated to use win.move(y, x)
    """
    # if its in the text field
    if cursorPos == -1:
        win.addstr(start+1, 10+tbCursor, "")
    else:
        found_line = False
        lineCount = start + 4
        index = 0

        for item in todoList:
            if index == cursorPos:
                win.addstr(lineCount, 4, "")
                found_line = True
                break
            else:
                lineCount += len(get_line_split(item))
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
                    lineCount += len(get_line_split(item))
                index += 1






def print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo, logo, noDate):
    """
        Prints all three UI elements to the curses window, logo, new todo Input and the todo list
    """
    linesUsed = print_logo(win, 0,0, logo, noDate)
    print_new_todo_input(win, newTodo, tbCursor, textField, linesUsed)
    print_todo(win, todoList, doneList, cursorPos, linesUsed)

    updateCursor(win, cursorPos, tbCursor, todoList, doneList, linesUsed)

