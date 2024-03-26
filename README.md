# lab3.py User Manual

This is the User Manual of the lab3.py that shows every modification done to a specific folder on your PC.
In order to run the lab3.py without any problems, you should follow these steps:

1. Open your editor. It is mandatory to have an installed Python compiler. **Online compilers DON'T WORK** as I have tested.

2. Once the editor is set up with the right compiler, open a new python file and paste the code in.

3. Search for line 8 where is the **FOLDER_PATH**, you must replace the string with your desired folder path.

4. after that you should go to that specified folder path and create a folder named **"SnapShots"**, dont worry this file wont be treated as a file from the specified folder.

5. If you run VSCode, there shouldn't be any problems in Problems field,but if you have never made any snapshot there will be a warning that no snapshot has been made,you should use the action 'commit' and continue like normal.

6. Run the code.

7. On the terminal, there should appear: **"Enter action (commit | info | status | exit): "** (The way you enter a option is not case senzitive. You can type InFO or sTaTUs the program will detect it as info or status).

8. Type "Info" with no parameter it will show the information about files in the current checked snapshot,      if you write a parameter like a filename example **"test.txt"** it will show only about that file (!!! Note: a filename should be written with no capital letters because of a little "design choice", only the files with lowercase will be able to be read independently).      There are some kewords alocaded for: "commit" or "c" for printing the entire list of files from the current commited snapshot

9. Type "Status" with no parameter it will show the file changes from the previous snapshot to the current snapshot.    Here are also some reserved keywords and they are: "commit" and "c" that will show the changes between the last snapshot commited and the current snapshot that was checked.(!!! Note: files that have been changed will show, while the files with no change will not be shown)
10. Type "commit" with no parameter in order to save the current snapshot as a commited. The same as the previous actions, here are the reserved keywords: "last" or "l' will go back one saved commit (going back in time) while on the other side "next" or "n" will go forward in time (is limited only to the last submitted commit by the user AKA the present, of course we dont wand you to read the future)
11. Type "Exit" in order to exit the program (it may take a few seconds)

That's all you need to do in order to use this program. here is some information about the program.
This program is made to show every change in a folder **WINDOWS Only**.
The folder can be changed by replacing the FOLDER_PATH variable in line 8.
The program checks every 5 seconds, no matter when you change the files in the folder, the program will notify you about the changes it the terminal.


## Program features:
1. New files are detected, they are shown in the terminal.
2. Deleted files are shown in the terminal when a check happends.
3. Modified files are shown in the terminal similar to the new or deleted files.
4. There is a SnapShots folder in the folder that you have specified to save the snapshots that will be taken,and it wont be ckecked as being apart of the folder.
5. It's fairly easy to modify it, for example to introduce a custom folder location.
6. With more advanced skills, there can be implemented a better way to save the snapshots, or even a batch verification system.

This is what you need to know in order to use this program.
In the future probably it will be updated with better console interacability. 
