from . import sql

def getParameter(includeAccount, includeContents, includeChats):
    parameters = {}
    if includeAccount:
        parameters["account"] = sql.getAccount()
    if includeContents:
        parameters["contents"] = sql.getContents()
    if includeChats:
        parameters["chats"] = sql.getChats()
    return parameters