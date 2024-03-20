import os
import time
import threading
import json

FOLDER_PATH = "E:\\TEMPORARE\\Catalin_OOP\\MyGit"
SNAPSHOT_FOLDER = os.path.join(FOLDER_PATH, "SnapShots")
SNAPSHOT_TIME = None
CurrentSnapshot = []
LastSnapshot = []
FILE_CURRENT_LIST = []
FILE_NAME_LIST = os.listdir(FOLDER_PATH)

class FileInfo:
    def __init__(self, filename, size, created, modified):
        self.filename = filename
        self.size = size
        self.created = created
        self.modified = modified

def get_meta_info(filename):
    filepath = os.path.join(FOLDER_PATH, filename)
    if not os.path.exists(filepath):
        print(f"File '{filename}' not found.")
        return None

    stat = os.stat(filepath)
    file_info = FileInfo(
        filename=filename,
        size=stat.st_size,
        created=time.ctime(stat.st_ctime),
        modified=time.ctime(stat.st_mtime)
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
            modified=item['modified']
        )
        file_info_list.append(file_info)
    return file_info_list

def print_file_info(file_list):
    if file_list:
        print("not empty")
    else:
        print("empty")

    for file in file_list:
        print(f"File:  {file.filename} \t\t {file.size} bytes \t\t Ct: {file.created} \t\t Md: {file.modified}")

def check_modified_objects():
    global CurrentSnapshot
    global LastSnapshot

    ##last_snapshot_dict = {file_info.filename: file_info for file_info in LastSnapshot}
    ##current_snapshot_dict = {file_info.filename: file_info for file_info in CurrentSnapshot}

    # Check modified and new files
    for filename, current_file_info in CurrentSnapshot:
        if filename in LastSnapshot:
            # Compare modified timestamp
            if current_file_info.modified != LastSnapshot[filename].modified or current_file_info.size != LastSnapshot[filename].size:
                print(f"{filename} - Has been modified")
        else:
            print(f"{filename} - New file")

    # Check deleted files
    for filename, last_file_info in LastSnapshot:
        if filename not in CurrentSnapshot:
            print(f"{filename} - Has been deleted")



while True:  # main
    LastSnapshot = CurrentSnapshot = read_snapshot("Snapshot.json") # incarcarea la inceput de program
    
    action = input("Enter action (commit | info | status | exit): ").strip().lower()
    
    if action == "commit":
        save_a_snapshot("Snapshot.json")
    
    elif action == "info":
        print_file_info(CurrentSnapshot)
    
    elif action == "status":
        LastSnapshot = CurrentSnapshot
        CurrentSnapshot = Search()
        #print_file_info(CurrentSnapshot)
        check_modified_objects()
        
    elif action == "exit":
        print("Exiting program.")
        break
    else:
        print("Invalid action. Available actions: (commit | info | status | exit)")
