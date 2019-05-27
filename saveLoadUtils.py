import os
import json


def save_to_file(todoList, doneList):
    """ 
        Save the current todoList to the ~/todosave file
    """

    filePath = os.path.expanduser('~/todoSave')
    f = open(filePath, 'w+')
    # wipe the old save file
    f.truncate(0)


    obj = {"todo": todoList, "done": doneList}
    f.write(json.dumps(obj, indent=4))


def loadFromFile():
    """
        Load the current todoList from the ~/todosave file
    """

    # if we cant get a file, return empty arrays
    try:
        filePath = os.path.expanduser('~/todoSave')
        fileContents = open(filePath, 'r').read()
        todoList = json.loads(fileContents)["todo"]
        doneList = json.loads(fileContents)["done"]

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
