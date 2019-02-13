def save_to_file(todoList, doneList):
    f = open("todoSave", 'w+')
    # wipe the old save file
    f.truncate(0)

    todoString = ",".join(todoList)
    if todoString == ",": todoString = ""

    doneString = ",".join(doneList)
    if doneString == ",": doneString = ""

    output = todoString + ";" + doneString
    f.write(output)


def loadFromFile():
    try:
        line = open("todoSave", 'r').read()
        todoList = line.split(';')[0].split(',')
        doneList = line.split(';')[1].split(',')

        todoListFiltered = []
        doneListFiltered = []

        for item in todoList:
            if "[ ]" in item:
                todoListFiltered.append(item)

        for item in doneList:
            if "[ ]" in item:
                doneListFiltered.append(item)

        return todoListFiltered, doneListFiltered
    except:
        return [], []
