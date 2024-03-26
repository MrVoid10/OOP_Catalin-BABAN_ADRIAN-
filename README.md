**lab3.py User Manual**

This is the User Manual of the lab3.py that shows every modification done to a specific folder on your PC.
In order to run the lab3.py without any problems, you should follow these steps:

1. Open your editor. It is mandatory to have an installed Python compiler. **Online compilers DON'T WORK** as I have tested.
2. Once the editor is set up with the right compiler, open a new python file and paste the code in.
3. Search for line 7 where is the **FOLDER_PATH**, you must replace the string with your desired folder path.
4. after that you should go to that specified folder path and create a folder named **"SnapShots"**.
5. If you run VSCode, there shouldn't be any problems in Problems field,but if you have never made any snapshot there will be a warning that no snapshot has been made,you should use the action 'commit' and continue like normal.
6. Run the code.
7. On the terminal, there should appear: **"Enter action (commit | info | status | exit): "** (The way you enter a option is not case senzitive. You can type InFO or sTaTUs the program will detect it as info or status).
8. Type "Info" in order to show the information about files in the current snapshot (Note that this snapshot isn't the current commit, this is the last change in the directory but not commited ).
9. Type "Status" in order to show the file changes from the last commit (files that have been changed will show, while the files with no change will not be shown) .
10. Type "commit" in order to save the current snapshot as a commit  
11. Type "Exit" in order to exit the program (it may take a few seconds)

That's all you need to do in order to use this program. here is some information about the program.
This program is made to show every change in a folder **WINDOWS Only**.
The folder can be changed by replacing the FOLDER_PATH variable in line 7.
The program checks every 5 seconds, no matter when you change the files in the folder, the program will notify you about the changes only 1 time it the terminal.


Program features:
1. New files are detected, they are shown in the terminal.
2. Deleted files are shown in the terminal when a check happends.
3. Modified files are shown in the terminal similar to the new or deleted files.
4. There is a SnapShots folder in the folder that you have specified to save the snapshots that will be taken.
5. It's fairly easy to modify it, for example to introduce a custom folder location.
6. With more advanced skills, there can be implemented a better way to save the snapshots, or even a batch verification system.

This is what you need to know in order to use this program.
In the future probably it will be updated with better console interacability. 
