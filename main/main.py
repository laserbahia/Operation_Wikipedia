import sys
import codecs
import customtkinter
from customtkinter import *
import requests
import subprocess
import json
from get_linked_articles import get_important_links, find_duplicate_values
import pickle
import keyboard
import threading  
import io

# Set stdout to write in UTF-8 encoding
sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())

#define variables
article_to_be_searched = ""
linked_articles = []

#define functions
def handle_escape():
    def on_esc_press(e):
        print("Escape key pressed. Exiting...")
        print("\n\n\n\n")
        print("Bye have a good day :)")
        print("for a time reference, look further down in the terminal")
        root.destroy()# Destroy the root window
        
        

    keyboard.on_press_key("esc", on_esc_press) #call the on_esc_press function, when esc is pressed

# Start listening for the Escape key in a separate thread
threading.Thread(target=handle_escape).start()

def search_btn_clicked():
    global linked_articles
    global article_to_be_searched
    global links_of_linked_articles
    global links_in_links
    # Get the text entered in the entry widget
    article_title = entry.get()
    if article_title == "":  # Check if the entry is empty
        global window
        window = CTk()  # Create a new window
        window.update()  # Force GUI update
        window.title("Error")
        label = customtkinter.CTkLabel(window, text="Please type in a Wikipedia article")
        label.pack(pady=10)
        ok_button = customtkinter.CTkButton(window, text="OK", command=close_window)
        ok_button.pack(pady=5)
        return  # Exit the function

    # Set the global variables for the article title and linked articles
    article_to_be_searched = article_title
    linked_articles, links_of_linked_articles = get_important_links(article_title,hoop_distance,True)
    print("number of hoops: ", str(hoop_distance)) 
    if linked_articles == [] :  # Check if the list of linked articles is empty
        window = CTk()  # Create a new window
        window.update()  # Force GUI update
        window.title("Error")
        label = customtkinter.CTkLabel(window, text="Article wasn't found, remember to use English")
        label.pack(pady=10)
        ok_button = customtkinter.CTkButton(window, text="OK", command=close_window)
        ok_button.pack(pady=5)
        return  # Exit the function
    links_in_links = find_duplicate_values(links_of_linked_articles)  # Find duplicate links in the linked articles
    print("Those are the  finite links in links: ",links_in_links,"\n\n\n")
    # Call the function to save articles to file
    save_articles_to_file()
    # Define the file name for the GUI
    file_name_gui = "main/gui_v5.py" #probably have to add main/ or remove the main/
    subprocess.Popen([sys.executable, file_name_gui])
    # Destroy the root window
    root.destroy()

def close_window():
    window.destroy()

def save_articles_to_file():
    # Print the links of linked articles
    print(links_of_linked_articles)
    # Write the article title and linked articles to separate text files
    with io.open("main/txt_files/article_to_be_searched.txt", "w", encoding="utf8") as f1, io.open("main/txt_files/linked_articles.txt", "w", encoding="utf8") as f2:
        article_data = {"article_to_be_searched": article_to_be_searched, "linked_articles": linked_articles}
        f1.write(article_data["article_to_be_searched"])
        for linked_article in article_data["linked_articles"]:
            f2.write(f"{linked_article}\n")
    # Serialize and write the links of linked articles and duplicate links to separate pickle files
    with open("main/txt_files/linked_linked_articles.pkl","wb") as f3:
        pickle.dump(links_of_linked_articles, f3) 
        print("Links in links:", links_of_linked_articles)

    with open("main/txt_files/linkes_in_links.pkl", "wb") as f4:
        pickle.dump(links_in_links, f4)

def update_hoop_distance(value):
    global hoop_distance
    hoop_distance = value
    label_var.set(f"Hoop Distance: {hoop_distance:.2f}")

if __name__ == "__main__":
    
    # Create the customtkinter window
    root = customtkinter.CTk()  # create window 
    root.title("Graph Generator")
    root.resizable(width=False, height=False)

    #defining screen size variables
    window_height = 100
    window_width = 290
    root.geometry(f"{window_width}x{window_height}") 
    

    entry = customtkinter.CTkEntry(root, placeholder_text="Which article do you want to  search?", width=230, height=15)  # define Entry for Article search
    entry.pack()

    hoop_distance = 2
    label_var = StringVar()
    label = customtkinter.CTkLabel(root, textvariable=label_var)
    label_var.set(f"Hoop Distance: {hoop_distance:.2f}")
    label.pack()

    slider = CTkSlider(root, from_=0, to=5, command=update_hoop_distance, number_of_steps=5)
    slider.pack()
    slider.set(2)

    search_btn = customtkinter.CTkButton(root, text="search", command=search_btn_clicked)  # define search btn
    search_btn.pack()


    root.mainloop()
