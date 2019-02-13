import os

def save_to_file(todoList, doneList):
    """ 
        Save the current todoList to the ~/todosave file
    """

    filePath = os.path.expanduser('~/todoSave')
    f = open(filePath, 'w+')
    # wipe the old save file
    f.truncate(0)

    todoString = ",".join(todoList)
    if todoString == ",": todoString = ""

    doneString = ",".join(doneList)
    if doneString == ",": doneString = ""

    output = todoString + ";" + doneString
    f.write(output)


def loadFromFile():
    """
        Load the current todoList from the ~/todosave file
    """

    # if we cant get a file, return empty arrays
    try:
        filePath = os.path.expanduser('~/todoSave')
        line = open(filePath, 'r').read()
        todoList = line.split(';')[0].split(',')
        doneList = line.split(';')[1].split(',')

        todoListFiltered = []
        doneListFiltered = []

        # we want to filter any non formatted "[ ] ..." strings from the list as they are errors
        for item in todoList:
            if "[ ]" in item:
                todoListFiltered.append(item)

        for item in doneList:
            if "[ ]" in item:
                doneListFiltered.append(item)

        return todoListFiltered, doneListFiltered
    except:
        return [], []
