import os
import time
import threading
import json
import struct
import datetime

FOLDER_PATH = "E:\TEMPORARE\Catalin_OOP\MyGit"
SnapListName = "CommitList.json"
TreePos = -1
SNAPSHOT_FOLDER = os.path.join(FOLDER_PATH, "SnapShots")
SNAPSHOT_TIME = None
CurrentSnapshot = []
CurrentCommit = []
LastSnapshot = []
FILE_CURRENT_LIST = []
FILE_NAME_LIST = os.listdir(FOLDER_PATH)

class FileInfo:
    def __init__(self, filename, size, created, modified,specific):
        self.filename = filename
        self.size = size
        self.created = created
        self.modified = modified
        self.specific = specific

class Snapshot:
    def __init__(self):
        self.time = time.time()
        self.file_info_list = []

class SnapListEncoder(json.JSONEncoder):
    def default(self, obj):
        entry = dict(obj.__dict__)
        entry['__class__'] = obj.__class__.__name__
        return entry

class SnapListDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, dictionary):
        if dictionary.get("__class__") == "FileInfo":
            obj = FileInfo.__new__(FileInfo)
        elif dictionary.get("__class__") == "Snapshot":
            obj = Snapshot.__new__(Snapshot)
        else:
            return dictionary

        for key, value in dictionary.items():
            if key != '__class__':
                setattr(obj, key, value)
        return obj

def get_meta_info(filename):
    if filename == "SnapShots":
        return None
    filepath = os.path.join(FOLDER_PATH, filename)
    
    if not os.path.exists(filepath):
        print(f"File '{filename}' not found.")
        return None

    stat = os.stat(filepath)
    spec = ""
    
    if filename.lower().endswith((".png", ".jpg")):
        with open(filepath, "rb") as img_file:
            img_data = img_file.read(24)
            width,height = struct.unpack(">II", img_data[16:24])
        spec = str(width) + ' X ' + str(height)
        #spec = "Imagine"
    elif filename.lower().endswith((".txt", ".py")):
        with open(filepath, "r") as file:
            read = file.read()
            spec = str(len(read.splitlines())) + " Linii " + str(len(read.split())) + " cuvinte " + str(len(read)) + " Caractere"

    file_info = FileInfo(
        filename=filename,
        size=stat.st_size,
        created=time.ctime(stat.st_ctime),
        modified=time.ctime(stat.st_mtime),
        specific= spec
    )
    return file_info

def Search():
    file_info_list = []  # a list of FileInfo objects
    file_name_list = os.listdir(FOLDER_PATH)
    
    for file_name in file_name_list:
        file_info = get_meta_info(file_name)
        if file_info:  # Check if get_meta_info() returned a valid FileInfo object
            file_info_list.append(file_info)
#    RETURN_LIST = file_info_list
    return file_info_list

def print_file_info(file_list):
    if file_list:
        for file in file_list:
            print(f"File: {file.filename}    {file.size} bytes  Ct: {file.created}    Md: {file.modified}   Specific: {file.specific}")
    else:
        print("empty List")

def print_file_info_1(file_list,name):
    if file_list:
        for file in file_list:
            if name == file.filename:
                print(f"File: {file.filename}    {file.size} bytes  Ct: {file.created}    Md: {file.modified}   Specific: {file.specific}")
    else:
        print("empty List")
def check_modified_objects(FirstList, LastList):
    last_filenames = {file_info.filename for file_info in LastList}
    #print("Check 5 Second")
    
    for current_file_info in FirstList:
        if current_file_info.filename not in last_filenames:
            print(f"{current_file_info.filename} - New file")
        else:
            last_file_info = next(file_info for file_info in LastList if file_info.filename == current_file_info.filename)
            if current_file_info.modified != last_file_info.modified or current_file_info.size != last_file_info.size or current_file_info.specific !=last_file_info.specific:
                print(f"{current_file_info.filename} - Has been modified")

    # Check deleted files
    for last_file_info in LastList:
        if last_file_info.filename not in {file_info.filename for file_info in FirstList}:
            print(f"{last_file_info.filename} - Has been deleted")

def repeat_check():
    global LastSnapshot, CurrentSnapshot  # Declare them as global
    while True:
        LastSnapshot = CurrentSnapshot
        CurrentSnapshot = Search()  # Replace with your actual Search function
        check_modified_objects(CurrentSnapshot, LastSnapshot)
        time.sleep(5)

def SaveAllCommits(tree):
    with open(os.path.join(SNAPSHOT_FOLDER,SnapListName), 'w') as file:
        json.dump(tree, file, cls=SnapListEncoder)

def LoadAllCommits():
    with open(os.path.join(SNAPSHOT_FOLDER,SnapListName), 'r') as file:
        tree = json.load(file, cls=SnapListDecoder)
    return tree


tree = []
try:
    tree = LoadAllCommits()
    CurrentCommit = LastSnapshot = CurrentSnapshot = tree[TreePos].file_info_list
    SNAPSHOT_TIME = tree[TreePos].time
except:
    print("Warning: the snapshots couldnt be loaded, prease use 'commit' to save a snapshot")
thread = threading.Thread(target=repeat_check, daemon=True)
thread.start()

while True:  # main
    action = input("Enter action (commit | info | status | exit): ").strip().lower()
    
    if action.startswith("commit"):
        words = action.split()
        if len(words) > 1:
            other_word = words[1]
            if other_word == "last" or other_word == "l":
                TreePos -=1
                CurrentCommit = tree[TreePos].file_info_list
                NAPSHOT_TIME = tree[TreePos].time
                dt_object = datetime.datetime.fromtimestamp(SNAPSHOT_TIME)
                print("Loaded previous commit on the date: " + dt_object.strftime("%Y-%m-%d %H:%M:%S"))
            elif other_word == "next" or other_word == "n":
                TreePos +=1
                if  TreePos < 0:
                    CurrentCommit = tree[TreePos].file_info_list
                    SNAPSHOT_TIME = tree[TreePos].time
                    dt_object = datetime.datetime.fromtimestamp(SNAPSHOT_TIME)
                    print("Loaded next commit on the date: " + dt_object.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    print("stop,you are at the last saved commit")
        else:
            T = Snapshot()
            CurrentCommit = CurrentSnapshot = Search()
            T.file_info_list = CurrentCommit
            tree.append(T)
            SaveAllCommits(tree)
    
    elif action.startswith("info"):
        words = action.split()
        if len(words) > 1:
            other_word = words[1]
            if other_word == "commit" or other_word == "c" :
                print_file_info(CurrentCommit)
            else:
                print_file_info_1(CurrentSnapshot,other_word)
        else:
            print_file_info(CurrentSnapshot)

    elif action.startswith("status"): # status between CurrentSnapshot and last Commit
        words = action.split()
        if len(words) > 1:
            other_word = words[1]
            if other_word == "commit" or other_word == "c":
                check_modified_objects(CurrentSnapshot,CurrentCommit)
        else:
            CurrentSnapshot = Search()
            check_modified_objects(CurrentSnapshot,LastSnapshot)

    elif action == "exit":
        print("Exiting program.")
        break
    else:
        print("Invalid action. Available actions: (commit | info | status | exit)")
