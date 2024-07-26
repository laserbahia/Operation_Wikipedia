# Operation_Wikipedia
Wikipedia Graph Project:

Disclaimer before using the programm: 
You might receive the error, that the files you need to load aren't findable (the directory you trying to open is not existent). If this error occurs to you, you need to either remove all the main/ statements from where the files get loaded in or add the main/ statement into every file path that gets loaded in. 
For example:
with io.open("main/txt_files/article_to_be_searched.txt", "r") as f1: 
If the error occurs in this state, you need to change it to the following: 
with io.open("txt_files/article_to_be_searched.txt", "r") as f1.
and the other way around.

The following lines indicate where to find the loading lines of code in the corresponding file:
Main.py : 
- lines: 73, 85, 91, 95

gui_v5.py:
- lines: 17, 25, 27, 30, 33, 92
