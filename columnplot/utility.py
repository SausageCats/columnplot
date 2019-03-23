import os


def file_exists(path, msg=None):
    if not os.path.exists(path):
        if msg:
            print(msg)
        else:
            print("File does not exist : ", path)
        exit(1)
    return True
