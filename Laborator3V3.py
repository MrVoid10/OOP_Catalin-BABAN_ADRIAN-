import os
import time
import threading
import json

FOLDER_PATH = "E:\\TEMPORARE\\Catalin_OOP\\MyGit"
SNAPSHOT_TIME = None
DETECTION_INTERVAL = 5
FILE_LIST = []
SNAPSHOT_FOLDER = os.path.join(FOLDER_PATH, "SnapShots")
COMMIT_FILE = os.path.join(SNAPSHOT_FOLDER, "commits.txt")

def create_snapshot_folder():
    if not os.path.exists(SNAPSHOT_FOLDER):
        os.makedirs(SNAPSHOT_FOLDER)

def commit():
    global SNAPSHOT_TIME
    global FILE_LIST
    SNAPSHOT_TIME = time.time()
    FILE_LIST = os.listdir(FOLDER_PATH)
    print("Snapshot time updated to:", time.ctime(SNAPSHOT_TIME))
    save_commits()

def get_file_info(filename):
    filepath = os.path.join(FOLDER_PATH, filename)
    if not os.path.exists(filepath):
        print(f"File '{filename}' not found.")
        return

    stat = os.stat(filepath)
    print(f"File: {filename}")
    print(f"Extension: {os.path.splitext(filename)[1]}")
    print(f"Created: {time.ctime(stat.st_ctime)}")
    print(f"Last modified: {time.ctime(stat.st_mtime)}")

    if filename.lower().endswith((".png", ".jpg")):
        print("Image file info (TODO):")
    elif filename.lower().endswith(".txt"):
        with open(filepath, "r") as file:
            lines = file.readlines()
            word_count = sum(len(line.split()) for line in lines)
            char_count = sum(len(line) for line in lines)
            print(f"Line count: {len(lines)}")
            print(f"Word count: {word_count}")
            print(f"Character count: {char_count}")
    elif filename.lower().endswith((".py", ".java")):
        print("Program file info (TODO):")
    else:
        print("Unsupported file type.")

def status_changes():
    if SNAPSHOT_TIME is None:
        print("Snapshot not taken yet. Use 'commit' to take a snapshot.")
        return

    current_files = os.listdir(FOLDER_PATH)
    for filename in FILE_LIST:
        if filename not in current_files:
            print(f"{filename} - File has been deleted or removed.")
        else:
            filepath = os.path.join(FOLDER_PATH, filename)
            stat = os.stat(filepath)
            if stat.st_mtime > SNAPSHOT_TIME:
                print(f"{filename} - Changed since snapshot.")

def status_all():
    if SNAPSHOT_TIME is None:
        print("Snapshot not taken yet. Use 'commit' to take a snapshot.")
        return

    print("Status (All Files):")
    current_files = os.listdir(FOLDER_PATH)
    for filename in FILE_LIST:
        if filename not in current_files:
            print(f"{filename} - File has been deleted or removed.")
        else:
            filepath = os.path.join(FOLDER_PATH, filename)
            stat = os.stat(filepath)
            if stat.st_mtime > SNAPSHOT_TIME:
                print(f"{filename} - Changed since snapshot.")
            else:
                print(f"{filename} - Unchanged.")

def save_commits():
    create_snapshot_folder()
    with open(COMMIT_FILE, "w") as f:
        f.write(f"Snapshot time: {time.ctime(SNAPSHOT_TIME)}\n")
        f.write("File list:\n")
        for filename in FILE_LIST:
            f.write(f"{filename}\n")
    print(f"Commits saved to {COMMIT_FILE}")

def load_commits():
    if os.path.exists(COMMIT_FILE):
        print(f"Loading commits from {COMMIT_FILE}")
        with open(COMMIT_FILE, "r") as f:
            lines = f.readlines()
            global SNAPSHOT_TIME
            global FILE_LIST
            SNAPSHOT_TIME = time.mktime(time.strptime(lines[0].split(":")[1].strip(), "%a %b %d %H:%M:%S %Y"))
            FILE_LIST = [line.strip() for line in lines[2:]]
            print("Commits loaded from file.")

def detect_changes():
    while True:
        time.sleep(DETECTION_INTERVAL)
        status_changes()

load_commits()

detection_thread = threading.Thread(target=detect_changes)
detection_thread.daemon = True
detection_thread.start()

while True:  # main
    action = input("Enter action (commit/info/status_all/status_changes/exit): ").strip().lower()
    if action == "commit":
        commit()
    elif action.startswith("info "):
        filename = action.split(maxsplit=1)[1]
        get_file_info(filename)
    elif action == "status_all":
        status_all()
    elif action == "status_changes":
        status_changes()
    elif action == "exit":
        print("Exiting program.")
        break
    else:
        print("Invalid action. Available actions: commit, info <filename>, status_all, status_changes, exit")