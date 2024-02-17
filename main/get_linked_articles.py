import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

global top_30_words_only_complete_dictionary
global counter
counter=0
top_30_words_only_complete_dictionary = {}
global links_in_links
links_in_links={}
global links_of_links
links_of_links={}



def get_important_links(article_title,hopping_distance,currently_hopping):
    global important_links
    global counter
    global links_in_links
    global links_of_links
    important_links = []
    global top_30_words_only_complete_dictionary
    linked_articles = get_linked_articles(article_title)
    backlinks = get_backlinks(article_title)
    navbox_titles = get_all_navbox_titles(article_title)

    #print(linked_articles)

    fresh_linked_articles = []

    for element in linked_articles:
        if element not in navbox_titles:
            fresh_linked_articles.append(element)


    #print("Updated linked articles: \n\n\n\n",fresh_linked_articles)

    for element in fresh_linked_articles:
        #print(element)
        if element in backlinks:
            important_links.append(element)
    
    #print("Those are the important_links: \n\n\n\n", important_links)
    
    if len(important_links) >=10 or currently_hopping == True:
        relevance = count_word_occurrences(important_links, article_title)
        #print("This is the relevance:", relevance)
    else:
        relevance = {}
        for important_article in fresh_linked_articles:
            relevance_number=0
            link_titles=[]
            linked_articles_important = get_linked_articles(important_article)
            for link in linked_articles_important:
                link_titles.append(link)
            for page in link_titles:
                if page == article_title:
                    relevance_number = relevance_number+1
            relevance[important_article]=relevance_number
        #print("This is the relevance: ", relevance)
    # Sort linked articles by relevance and retrieve the top 30
    #sorted_articles = sorted(relevance.items(), key=lambda x: x[1], reverse=True)
    #top_30_articles = [article[0] for article in sorted_articles[:30]]

    # Sorting the dictionary based on values in descending order
    sorted_words = sorted(relevance.items(), key=lambda x: x[1], reverse=True)

    # Selecting the top 30 words
    top_30_words = sorted_words[:2]

    # Only the words without their associated numbers
    top_30_words_only = [word[0] for word in top_30_words]


    print("Those are the ones that should be searched", top_30_words_only)
    top_30_words_only_complete_dictionary[article_title]=top_30_words_only

    if hopping_distance>0:
        for link in top_30_words_only:
            print("Currenly Checking: ",link)
            links_of_links[link]=get_important_links(link,hopping_distance-1,True)
        print("Those are the linked articles of the linked articles:", links_of_links)

    print("\n\n\n\n This is currently the dictionary: \n\n\n\n", top_30_words_only_complete_dictionary)
    
    print("Those are the links_in_links:", links_in_links)
    return top_30_words_only,links_of_links



def get_linked_articles(article_title):
    base_url = "https://en.wikipedia.org/w/api.php" #url for the api
    params = { # define parameters in api request
        'action': 'query', # query action, so retrieving information
        'titles': article_title, # information that is request
        'prop': 'links', # property of the page to retrieve information from
        'format': 'json', # response format
        'pllimit': 500, # set limit of returned links to maximum (500)
        'plgenerator': 'allpages',
        'gaplimit': 500,
    }

    
    global linked_articles
    global backlinks
    linked_articles = []
    backlinks = []

    response = requests.get(base_url, params=params)  # get request
    data = response.json()

    while True:
        response = requests.get(base_url, params=params) # get request
        data = response.json()
        response.raise_for_status()

        # Extract linked articles
        pages = data['query']['pages'] # accesses values associated to key "query" and then key "pages"
        for page_id in pages:
            page = pages[page_id] # get individual page object
            links = page.get('links', []) # if "links" key is present it returns value associated with it, otherwise the second parameter (empty list)
            linked_articles.extend(link['title'] for link in links) # extend list with titels of the links

       # Check if there are more results
        continue_param = data.get('continue', {}) # retrieves  "continue" parameter from "data" dictoinary (if doesn't exits returns empty dictionary)
        #print(continue_param)
        if not continue_param: # checks if contine_param is an empty list
            break

        # Update the params with the continue parameter
        params.update(continue_param)

        """
        Explanation of the "continue" key:

        This "continue" key and its value are typically 
        provided by an API to enable the client 
        to go through a large dataset in chunks.
        The value of the "continue" key is a token 
        that the client can use in a subsequent 
        request to retrieve the next chunk of items.
        The code checks if the continue parameter is 
        empty to determine if there are any more results 
        to retrieve.

        """

    filtered_links = [string for string in linked_articles if ':' not in string and "/" not in string]

    #print("\n\n\nFiltered links:", filtered_links)
    return filtered_links

def get_backlinks(article_title):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'backlinks', 
        'bllimit': 500,  # Maximum number of backlinks 
        'bltitle': article_title, #  Title of the page to get backlinks from
    }

    response = requests.get(base_url, params=params) # get request
    data = response.json()
    #print(data)

    # Extract linked articles
    backlinks = data['query']['backlinks'] # accesses values associated to key "query" and then key "backlinks"

    """
    code so titles with a ":" or "/" in them get ruled out, 
    because those are not articles but rather user talks, requests or collections of articles
    """
    filtered_backlinks = [page['title'] for page in backlinks if ':' not in page['title'] and '/' not in page['title']]

    #print("\n\n\nfiltered backlinks:", filtered_backlinks)
    return filtered_backlinks
    
def count_word_occurrences(articles, target_word):
    occurrences_dict = {}
    
    for article_title in articles:
        article_text = get_article_text(article_title)
        occurrences = article_text.count(target_word)
        occurrences_dict[article_title] = occurrences
    
    return occurrences_dict

def get_article_text(article_title):
    try:
        # Define the parameters for the API request
        params = {
            'action': 'query',
            'titles': article_title,
            'prop': 'extracts',
            'explaintext': True,
            'format': 'json',
        }

        # Make the API request
        response = requests.get('https://en.wikipedia.org/w/api.php', params=params)
        data = response.json()

        # Extract the text content of the article
        page_id = next(iter(data['query']['pages'].keys()))
        article_text = data['query']['pages'][page_id].get('extract', 'No extract available')

        return article_text

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    

def get_all_navbox_titles(article_title):
    # Fetch the Wikipedia article content
    url = f"https://en.wikipedia.org/wiki/{article_title}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all navbox sections (adjust based on Wikipedia article structure)
    navboxes = soup.find_all("div", {"class": "navbox"})

    # Extract article titles from all navboxes
    titles = []
    for navbox in navboxes:
        for link in navbox.find_all("a", href=re.compile(r"/wiki/")):
            title = link.get("title")
            if title:
                titles.append(title)

    return titles

def find_duplicate_values(data):
    value_keys = {}  # Dictionary to store keys associated with each value

    # Populate value_keys
    for key, (values, _) in data.items():
        for value in values:
            if value in value_keys:
                value_keys[value].append(key)
            else:
                value_keys[value] = [key]

    # Filter out duplicates
    duplicate_pairs = {value: keys for value, keys in value_keys.items() if len(keys) > 1}

    return duplicate_pairs

"""
#Example usage
article_title = "Sursee"
linked_articles = get_linked_articles(article_title)
backlinks = get_backlinks(article_title)
print("Linked Articles: \n\n", linked_articles)
print("Backlinks: \n\n", backlinks)
print("\n\n\n\n Those are the important links: ", important_links)
"""
"""
article_title="Sursee"
important_links=get_important_links(article_title)
print("Those are the important links:", important_links)
"""



#Test

article_title = "Sempach"

#linked_articles = get_linked_articles(article_title)
#backlinks = get_backlinks(article_title)
#article_text = get_article_text(article_title)
#navbox_text = get_all_navbox_titles(article_title)
#linked_articles, links_of_linked_articles = get_important_links(article_title,2,True)
#links_in_links = find_duplicate_values(links_of_linked_articles)
#print("Linked Articles: \n\n", linked_articles)
#print("Backlinks: \n\n", backlinks)
#print("Article text: \n\n", article_text)
#print("NavboxText:, \n\n ",navbox_text)
#print("Important, \n\n", linked_articles)
#print("Links of linked articles, \n\n",links_of_linked_articles)
#print("Links in links: ",links_in_links)
