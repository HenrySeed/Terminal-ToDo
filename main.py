import curses
import curses.textpad
import os
from saveLoadUtils import *
from cursesUtils import setupColour
from logoUtils import printLogo

def tb_backSpace(text, index):
    return text[:index-1] + text[index:]


def tb_insert(text, key, cursor):
    return text[:cursor] + key + text[cursor:]


def toggle_todo(index, todoList, doneList):
    item = (todoList + doneList)[index]

    if index < len(todoList):
        del todoList[index]
        return [todoList, doneList+[item]]
    else:
        del doneList[index - len(todoList)]
        return [todoList+[item], doneList]


def remove_todo(index, todoList, doneList):
    if index < len(todoList):
        del todoList[index]
        return [todoList, doneList]
    else:
        del doneList[index - len(todoList)]
        return [todoList, doneList]


def print_new_todo(win, todo, tbCursor, active=False):
    todoString = todo
    win.addstr(8,0, "New TODO: " + todoString)
    if active:
        win.addstr(8,10 + tbCursor, "█")



def print_todo(win, listTodo, doneList, cursorLine):
    listX = 3
    listY = 10

    win.addstr(listY, 0, " TODO ------------------")
    # the y screen position of the start of the list

    listY += 1
    
    count = 0
    for todo in listTodo:
        if cursorLine == count:
            win.addstr(listY+count, listX, todo.replace('[ ]', "[█]"))
        else:
            win.addstr(listY+count, listX, todo)
        count += 1

    win.addstr(listY+count+1, 0, " DONE ------------------")
    # the y screen position of the start of the list
    listY += 2
    for todo in doneList:
        if cursorLine == count:
            win.addstr(listY+count, listX, todo.replace('[ ]', "[█]"))
        else:
            win.addstr(listY+count, listX, todo.replace('[ ]', "[x]"))
        count += 1

def print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo):
    printLogo(win, 0,0)
    print_todo(win, todoList, doneList, cursorPos)
    print_new_todo(win, newTodo, tbCursor, textField)



def main(win):
    # sets sursor to invisible
    curses.curs_set(0)
    win.nodelay(True)
    win.clear() 
    setupColour(win)

    todoList, doneList = loadFromFile()
    cursorPos = 0
    textField = False
    newTodo = ""
    tbCursor = 0

    # if we have empty lists, start the curser in the new item field
    if len(todoList + doneList) == 0:
        cursorPos = -1
        textField = True

    print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo)

    key = ""
    while 1:  
        try:
            key = win.getkey() 

            if textField:

                if key == "KEY_DOWN":
                    if len(doneList + todoList) > 0:
                        cursorPos += 1
                        textField = False

                elif key == "KEY_LEFT": 
                    if tbCursor > 0: tbCursor -= 1

                elif key == "KEY_RIGHT": 
                    if tbCursor < len(newTodo): tbCursor += 1

                elif ord(key) == 27:    # Escape
                    newTodo = ""
                    cursorPos += 1
                    textField = False
                    tbCursor = 0

                elif key == "\n":       # Enter
                    todoList.append("[ ] " + newTodo)
                    newTodo = ""
                    cursorPos += 1
                    textField = False
                    tbCursor = 0

                elif ord(key) == 127:   # Backspace
                    if tbCursor > 0: 
                        newTodo = tb_backSpace(newTodo, tbCursor)
                        tbCursor -= 1

                elif ord(key) >= 32 and ord(key) <= 254:
                    newTodo = tb_insert(newTodo, key, tbCursor)
                    tbCursor += 1

            else:
                if key == 'q':
                    return
                elif key == "KEY_UP":
                    cursorPos -= 1
                elif key == "KEY_DOWN":
                    cursorPos += 1
                elif ord(key) == 127:
                    todoList, doneList = remove_todo(cursorPos, todoList, doneList)
                    cursorPos -= 1
                    if cursorPos < 0 and len(doneList + todoList) > 0: cursorPos = 0
                elif key == "\n":
                    todoList, doneList = toggle_todo(cursorPos, todoList, doneList)

            # make sure we havent left the array
            if cursorPos < -1: 
                cursorPos = -1
                textField = True
            elif cursorPos == -1:
                textField = True
            elif cursorPos > len(todoList)+len(doneList) - 1:
                cursorPos = len(todoList)+len(doneList) - 1


            # Clear the window is always needed
            win.clear() 

            # win.addstr(34, 0, ' ' * 100)
            # win.addstr(34, 0, "Key: " + key + "cursorPos: " + str(cursorPos))

            print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo)


            save_to_file(todoList, doneList)

            # win.addstr(34, 0, ' ' * 100)
            # win.addstr(34, 0, str(todoList) +"    " +  str(doneList))

        except Exception as e:
            # No input   
            # if str(e) != 'no input':
            #     win.addstr(35, 0, ' ' * 100)
            #     win.addstr(35, 0, "ERROR: {0}".format(e))
            pass  

        


os.environ.setdefault('ESCDELAY', '25')
curses.wrapper(main)