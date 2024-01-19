import sys
import codecs
import customtkinter
from customtkinter import *
import requests
import subprocess
import json

# Add these lines at the beginning of your script
sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())

#define variables
article_to_be_searched = ""
linked_articles = []

#define functions
def get_linked_articles(article_title):
    global linked_articles
    base_url = "https://en.wikipedia.org/w/api.php"  # url for the api
    params = {  # define parameters in api request
        'action': 'query',  # query action, so retrieving information
        'titles': article_title,  # information that is request
        'prop': 'links',  # property of the page to retrieve information from
        'format': 'json'  # response format
    }

    response = requests.get(base_url, params=params)  # get request
    data = response.json()

    # Extract linked articles
    pages = data['query']['pages']  # accesses values associated to key "query" and then key "pages"
    for page_id in pages:
        links = pages[page_id].get('links', [])  # if "links" key is present it returns value associated with it, otherwise the second parameter (empty list)
        linked_articles.extend(link['title'] for link in links)  # extend list with titels of the links

    return linked_articles

def search_btn_clicked():
    global linked_articles
    global article_to_be_searched
    article_title = entry.get()
    article_to_be_searched = article_title
    linked_articles = get_linked_articles(article_title)
    save_articles_to_file()
    file_name_gui = "main\gui.py"
    subprocess.Popen([sys.executable, file_name_gui])
    root.destroy()
    print("Linked Articles:", linked_articles)


def save_articles_to_file():
    with open("article_to_be_searched.txt", "w") as f1, open("linked_articles.txt", "w") as f2:
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