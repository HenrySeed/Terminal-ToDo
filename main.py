import curses
import curses.textpad
import os
from saveLoadUtils import *
from cursesUtils import setupColour
import sys
from todoUI import print_UI


#  Author: Henry Seed
#  Date: 10/02/2019
#  +---------------------------------------------------+
#  |                                                   |
#  |     A cute CLI todo list to keep things simple    |
#  |                                                   |
#  +---------------------------------------------------+


def catch_args():
    """
        Catches given arguments to set a custom logo and toggle the date.
    """
    try:
        customLogo = sys.argv[1]
        noDate = sys.argv[2]

        return [customLogo, noDate]
    except:
        return ["", "False"]

    


def tb_backSpace(text, index):
    """
        Removes the character at the given index from the text param and returns it.
    """
    return text[:index-1] + text[index:]


def tb_insert(text, key, cursor):
    """ 
        Inserts the given key at the cursor position in text and returns text.
    """
    return text[:cursor] + key + text[cursor:]


def toggle_todo(index, todoList, doneList):
    """
        Toggles the item at the index on todoList or DoneList and returns both
    """
    item = (todoList + doneList)[index]

    if index < len(todoList):
        del todoList[index]
        return [todoList, doneList+[item]]
    else:
        del doneList[index - len(todoList)]
        return [todoList+[item], doneList]


def remove_todo(index, todoList, doneList):
    """
        Removes the item at the index on todoList or DoneList and returns both
    """
    if index < len(todoList):
        del todoList[index]
        return [todoList, doneList]
    else:
        del doneList[index - len(todoList)]
        return [todoList, doneList]



def main(win):
    """
        The main function. sets up the curses menu, variables and holds the main loop for key catches. Also handles most of the updating of state and text input etc.
    """
    # sets sursor to invisible
    curses.curs_set(0)
    win.nodelay(True)
    win.clear() 
    setupColour(win)
    
    #get args
    logo, noDate = catch_args()

    todoList, doneList = loadFromFile()
    cursorPos = 0
    textField = False
    newTodo = ""
    tbCursor = 0

    # if we have empty lists, start the curser in the new item field
    if len(todoList + doneList) == 0:
        cursorPos = -1
        textField = True

    print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo, logo, noDate)

    key = ""
    while 1:  
        try:
            key = win.getkey() 

            # If we are currently in text field mode, and char typed should be added to the newTodo var 
            if textField:
                # if the user hits the arrow doen, exit the field
                if key == "KEY_DOWN":
                    if len(doneList + todoList) > 0:
                        cursorPos += 1
                        textField = False
                # Move the cursor left
                elif key == "KEY_LEFT": 
                    if tbCursor > 0: tbCursor -= 1
                # Move the cursor right
                elif key == "KEY_RIGHT": 
                    if tbCursor < len(newTodo): tbCursor += 1
                # Leave the input field and clear it 
                elif ord(key) == 27:    # Escape
                    newTodo = ""
                    cursorPos += 1
                    textField = False
                    tbCursor = 0
                # Add the entered todo to the todo array
                elif key == "\n":       # Enter
                    todoList.append("[ ] " + newTodo)
                    newTodo = ""
                    cursorPos += 1
                    textField = False
                    tbCursor = 0
                # Backspace
                elif ord(key) == 127:   
                    if tbCursor > 0: 
                        newTodo = tb_backSpace(newTodo, tbCursor)
                        tbCursor -= 1
                # If any normal char is typed (ASCII) then add to to input string
                elif ord(key) >= 32 and ord(key) <= 254:
                    newTodo = tb_insert(newTodo, key, tbCursor)
                    tbCursor += 1

            # IF we arent in textfield move then the cursor is on the todoLists
            else:
                # Quit
                if key == 'q':
                    return
                # Move up the todoList
                elif key == "KEY_UP":
                    cursorPos -= 1
                # Move down the todoList
                elif key == "KEY_DOWN":
                    cursorPos += 1
                # Backspace removes the current todo
                elif ord(key) == 127:
                    todoList, doneList = remove_todo(cursorPos, todoList, doneList)
                    cursorPos -= 1
                    if cursorPos < 0 and len(doneList + todoList) > 0: cursorPos = 0
                # Enter toggles the current todo
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

            print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo, logo, noDate)

            save_to_file(todoList, doneList)

            # win.addstr(34, 0, ' ' * 100)
            # win.addstr(34, 0, str(todoList) +"    " +  str(doneList))

        except Exception as e:
            # No input   
            # if str(e) != 'no input':
            #     win.addstr(35, 0, ' ' * 100)
            #     win.addstr(35, 0, "ERROR: {0}".format(e))
            pass  

        

# so the excape key doesnt have a noticable delay
os.environ.setdefault('ESCDELAY', '25')
curses.wrapper(main)