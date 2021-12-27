import os


def parse_userid(userid):
    parsedID = userid.replace("<@!", "").replace(">", "")
    return parsedID


def load_token():
    with open(os.getcwd() + "/key.txt") as f:
        line = f.readline()

    return line
