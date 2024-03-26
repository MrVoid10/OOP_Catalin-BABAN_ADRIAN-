import os
import time
import threading
import json
import struct

FOLDER_PATH = "E:\TEMPORARE\Catalin_OOP\MyGit"
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

def save_a_snapshot(SAVE_NAME):
    global CurrentSnapshot
    
    CurrentSnapshot = Search() # salvat 
    snapshot_data = json.dumps([ob.__dict__ for ob in CurrentSnapshot], indent=2)

    snapshot_file_path = os.path.join(SNAPSHOT_FOLDER, SAVE_NAME)
    snapshot_time_path = os.path.join(SNAPSHOT_FOLDER, "Created.txt")
    
    snap = time.time()
    with open(snapshot_time_path, "w") as sTime:
        sTime.write(f"{time.ctime(snap)}\n")
        sTime.close()
    
    with open(snapshot_file_path, "w") as snapshot_file:
        snapshot_file.write(snapshot_data)
        print(f"Snapshot saved to {SAVE_NAME}") #test

def read_snapshot(SAVE_NAME):
    global SNAPSHOT_TIME
    snapshot_file_path = os.path.join(SNAPSHOT_FOLDER, SAVE_NAME)
    snapshot_time_path = os.path.join(SNAPSHOT_FOLDER, "Created.txt")

    with open(snapshot_time_path, 'r') as t:
        SNAPSHOT_TIME = t.read().strip()
        t.close

    with open(snapshot_file_path, 'r') as json_file:
        data = json.load(json_file)

    file_info_list = []

    for item in data:
        file_info = FileInfo(
            filename=item['filename'],
            size=item['size'],
            created=item['created'],
            modified=item['modified'],
            specific=item['specific']
        )
        file_info_list.append(file_info)
    return file_info_list

def print_file_info(file_list):
    if file_list:
        print("not empty")
    else:
        print("empty")

    for file in file_list:
        print(f"File: {file.filename}    {file.size} bytes  Ct: {file.created}    Md: {file.modified}   Specific: {file.specific}")

def check_modified_objects(FirstList, LastList):
    last_filenames = {file_info.filename for file_info in LastList}
    #print("Check 5 Second")
    
    for current_file_info in FirstList:
        if current_file_info.filename not in last_filenames:
            print(f"{current_file_info.filename} - New file")
        else:
            last_file_info = next(file_info for file_info in LastList if file_info.filename == current_file_info.filename)
            if current_file_info.modified != last_file_info.modified or current_file_info.size != last_file_info.size:
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

while True:  # main
    try:
        CurrentCommit = LastSnapshot = CurrentSnapshot = read_snapshot("Snapshot.json") # incarcarea la inceput de program
    except:
        print("Warning: No snapshot has been made, please to make a commit using the command 'commit' ")
    
    thread = threading.Thread(target=repeat_check, daemon=True)
    thread.start()

    action = input("Enter action (commit | info | status | exit): ").strip().lower()
    
    if action == "commit":
        save_a_snapshot("Snapshot.json")
    
    elif action == "info":
        print_file_info(CurrentSnapshot)
    
    elif action == "status": # status between CurrentSnapshot and last Commit
        CurrentSnapshot = Search()
        check_modified_objects(CurrentSnapshot,CurrentCommit)
        
    elif action == "exit":
        print("Exiting program.")
        break
    else:
        print("Invalid action. Available actions: (commit | info | status | exit)")
