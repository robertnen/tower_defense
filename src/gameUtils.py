def getFilePath(name: str, typePath: str):
    filePath = __file__
    filePath = filePath[:filePath.rfind('src')]

    filePath = filePath + typePath + name

    return filePath

def volumes(level: int):
    if level == 0:
        return 0
    if level == 1:
        return 0.1
    if level == 2:
        return 0.25
    if level == 3:
        return 0.5
    if level == 4:
        return 0.75
    return 1