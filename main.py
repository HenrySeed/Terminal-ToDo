import curses
import curses.textpad
import os
from saveLoadUtils import *
from cursesUtils import *
import sys
from todoUI import print_UI
from time import sleep


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
        noHelp = sys.argv[3]

        return [customLogo, noDate, noHelp]
    except:
        return ["", "False", "False"]


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


def editTodo(todoList, doneList, editedTodoisTodo, newTodo, cursorPos):
    """
        Opens the selected todo in the edit field at the top of the page
    """
    todoStr = ""
    editedTodoisTodo = False
    # Get the selected todo
    if cursorPos < len(todoList):
        todoStr = todoList[cursorPos]
        del todoList[cursorPos]
        editedTodoisTodo = True
    else:
        todoStr = doneList[cursorPos - len(todoList)]
        del doneList[cursorPos - len(todoList)]
        editedTodoisTodo = False

    newTodo = todoStr.replace('[ ] ', '', 1)
    return [todoList, doneList, editedTodoisTodo, newTodo]


def main(win):
    """
        The main function. sets up the curses menu, variables and holds the main loop for key catches. Also handles most of the updating of state and text input etc.
    """
    curses.curs_set(1)
    win.nodelay(True)
    win.clear() 
    setupColour(win)
    
    #get args
    logo, noDate, noHelp = catch_args()

    todoList, doneList = loadFromFile()
    cursorPos = 0
    textField = False
    newTodo = ""
    tbCursor = 0
    menuOpen = False

    editedTodoisTodo = True

    # if we have empty lists, start the curser in the new item field
    if len(todoList + doneList) == 0:
        cursorPos = -1
        textField = True

    print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo, logo, noDate, noHelp, menuOpen)

    lastRows, lastCols = os.popen('stty size', 'r').read().split()

    key = ""
    while 1:  
        try:
            key = win.getkey() 

            keyNum = -20
            try:
                keyNum = ord(key)
            except:
                keyNum = -20

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
                elif keyNum == 27:    # Escape
                    # newTodo = ""
                    # cursorPos += 1
                    # textField = False
                    # tbCursor = 0
                    if newTodo.strip() != "":
                        if editedTodoisTodo:
                            todoList.append("[ ] " + newTodo)
                        else:
                            doneList.append("[ ] " + newTodo)
                        save_to_file(todoList, doneList)

                    return
                # Add the entered todo to the todo array
                elif key == "\n":       # Enter
                    if editedTodoisTodo:
                        todoList.append("[ ] " + newTodo)
                    else:
                        doneList.append("[ ] " + newTodo)
                    editedTodoisTodo = True
                    newTodo = ""
                    cursorPos += 1
                    textField = False
                    tbCursor = 0
                # Backspace
                elif keyNum == 127 or key == "KEY_BACKSPACE":   
                    if tbCursor > 0: 
                        newTodo = tb_backSpace(newTodo, tbCursor)
                        tbCursor -= 1
                # If any normal char is typed (ASCII) then add to to input string
                elif keyNum >= 32 and keyNum <= 254:
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
                # Edit the todo item
                if key == 'e':
                    textField = True
                    todoList, doneList, editedTodoisTodo, newTodo = editTodo(todoList, doneList, editedTodoisTodo, newTodo, cursorPos)
                    cursorPos = -1
                    tbCursor = len(newTodo)
                # Backspace removes the current todo
                elif keyNum == 127 or key == "KEY_BACKSPACE":
                    todoList, doneList = remove_todo(cursorPos, todoList, doneList)
                    cursorPos -= 1
                    if cursorPos < 0 and len(doneList + todoList) > 0: cursorPos = 0
                # Enter toggles the current todo
                elif key == "\n":
                    todoList, doneList = toggle_todo(cursorPos, todoList, doneList)
                elif keyNum == 27:
                    return;
                # Tab
                elif keyNum == 9:   
                    menuOpen = not menuOpen
                
            
                
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

            height, width = win.getmaxyx()


            # win.addstr(height - 3, 0, ' ' * 100)
            # win.addstr(height - 3, 0, "Key: " + key + " cursorPos: " + str(cursorPos))

            print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo, logo, noDate, noHelp, menuOpen)
            save_to_file(todoList, doneList)



        except Exception as e:
            height, width = win.getmaxyx()
            if height != lastRows or width != lastCols:
                lastRows, lastCols = height, width
                win.clear()
                print_UI(win, todoList, doneList, cursorPos, tbCursor, textField, newTodo, logo, noDate, noHelp, menuOpen)


            # No input 
            sleep(0.01)  

            # if str(e) != 'no input':
            #     win.addstr(height - 2, 0, ' ' * 100)
            #     win.addstr(height - 2, 0, "ERROR: {0}".format(e))
            pass  

        

# so the excape key doesnt have a noticable delay
os.environ.setdefault('ESCDELAY', '25')
curses.wrapper(main)