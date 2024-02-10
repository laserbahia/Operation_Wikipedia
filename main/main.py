import sys
import codecs
import customtkinter
from customtkinter import *
import requests
import subprocess
import json
from get_linked_articles import get_important_links

# Add these lines at the beginning of your script
sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())

#define variables
article_to_be_searched = ""
linked_articles = []

#define functions

def search_btn_clicked():
    global linked_articles
    global article_to_be_searched
    article_title = entry.get()
    article_to_be_searched = article_title
    linked_articles = get_important_links(article_title)
    save_articles_to_file()
    file_name_gui = "gui.py" #probably have to add a \main here at the front, depends on the path
    subprocess.Popen([sys.executable, file_name_gui])
    root.destroy()
    print("Linked Articles:", linked_articles)


def save_articles_to_file():
    with open("article_to_be_searched.txt", "w", encoding="utf8") as f1, open("linked_articles.txt", "w", encoding="utf8") as f2:
        article_data = {"article_to_be_searched": article_to_be_searched, "linked_articles": linked_articles}
        f1.write(article_data["article_to_be_searched"])
        for linked_article in article_data["linked_articles"]:
            f2.write(f"{linked_article}\n")

if __name__ == "__main__":
#customtkinter window 
    root = CTk()  # create window 

    entry = customtkinter.CTkEntry(root, placeholder_text="Which article do you wanna search?", width=225, height=15)  # define Entry for Article search
    entry.pack()

    search_btn = CTkButton(root, text="search", command=search_btn_clicked)  # define search btn
    search_btn.pack()

    root.mainloop()
