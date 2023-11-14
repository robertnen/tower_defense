def getFilePath(name: str, typePath : str):
    filePath = __file__
    filePath = filePath[:filePath.rfind('src')]

    filePath = filePath + typePath + name

    return filePath