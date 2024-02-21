import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict 

# Global variables to store dictionaries and counters
global top_x_words_only_complete_dictionary
global counter
counter=0
top_x_words_only_complete_dictionary = {}
global links_in_links
links_in_links={}
global links_of_links
links_of_links={}
global backlinks
backlinks = [] # Initialize list to store backlinks

# Function to get important links 
def get_important_links(article_title,hopping_distance,currently_hopping):
    global important_links
    global counter
    global links_in_links
    global links_of_links
    important_links = [] # Initialize list to store important links
    global top_x_words_only_complete_dictionary
    linked_articles = get_linked_articles(article_title) # Get linked articles
    backlinks = get_backlinks(article_title) # Get backlinks
    navbox_titles = get_all_navbox_titles(article_title) # Get titles from navbox

    excluding_navbox_titles = [] #list to store the linked articles excluding navbox_titles (just general links which aren't really relevant, we use that list if there are not enough backlinks)

    # Filter out navbox titles from linked articles
    for element in linked_articles:
        if element not in navbox_titles:
            excluding_navbox_titles.append(element)

    # Check if fresh linked articles are also backlinks, add them to important links (for better efficiency)
    for element in excluding_navbox_titles:
        if element in backlinks:
            important_links.append(element)
    
    # If there are enough important links or currently hopping, calculate relevance (when counting the word occurences the process is faster, so if we are hooping we want to choose the fastest way)
    if len(important_links) >=10 or currently_hopping == True:
        relevance = count_word_occurrences(important_links, article_title)
    else:
        #calculate relevance by again retrieving the linked articles of the important_articles
        relevance = {}
        for important_article in excluding_navbox_titles:
            relevance_number=0
            link_titles=[]
            linked_articles_important = get_linked_articles(important_article)
            for link in linked_articles_important:
                link_titles.append(link)
            for page in link_titles:
                if page == article_title:
                    relevance_number = relevance_number+1
            relevance[important_article]=relevance_number

    # Sorting the dictionary based on values in descending order
    sorted_words = sorted(relevance.items(), key=lambda x: x[1], reverse=True) #makes a lambda function (key=lamda...), gets specifies that sorting should be based on the second element (index1) of each tuple (lambda gets x as argumetn and returns x[1])

    # Selecting the top number of words specified in the article_count value
    article_count = 3
    top_x_words = sorted_words[:article_count]

    # Only the words without their associated numbers
    top_x_words_only = [word[0] for word in top_x_words]

    # store the most relevant links of all the articles in a dictiononary, key article title, values article links
    top_x_words_only_complete_dictionary[article_title]=top_x_words_only

    # If hopping distance is greater than 0, recursively get important links for top 30 words
    if hopping_distance>0:
        for link in top_x_words_only:
            links_of_links[link]=get_important_links(link,hopping_distance-1,True)
    
    # return both the linked articles of the main articel (top_x_words_only) aswell as the linked articles of the links (links_of_links)
    return top_x_words_only,links_of_links

# Function to get linked articles from Wikipedia
def get_linked_articles(article_title):
    base_url = "https://en.wikipedia.org/w/api.php" # Base URL for Wikipedia API
    params = { # Parameters for the API request
        'action': 'query', # Query action to retrieve information
        'titles': article_title, # Title of the article
        'prop': 'links', # Property to retrieve links
        'format': 'json', # Response format
        'pllimit': 500, # Maximum number of links
        'plgenerator': 'allpages', # Generator parameter specifying to retrieve links from all pages
        'gaplimit': 500, # Maximum number of pages to generate links from
    }

    global linked_articles
    linked_articles = [] # Initialize list to store linked articles

    response = requests.get(base_url, params=params)  # Send GET request to Wikipedia API
    data = response.json()

    # Iterate through the response data to extract linked articles
    while True:
        response = requests.get(base_url, params=params) # Send GET request
        data = response.json()
        response.raise_for_status()

        pages = data['query']['pages'] # Access pages from the response
        for page_id in pages:
            page = pages[page_id] # Get individual page object
            links = page.get('links', []) # Get links from the page
            linked_articles.extend(link['title'] for link in links) # Extend list with titles of the links

       # Check if there are more results
        continue_param = data.get('continue', {}) # Get continue parameter
        if not continue_param: # Check if continue parameter is empty
            break

        # Update the params with the continue parameter
        params.update(continue_param)

    # Filter out links with ":" or "/" in them
    filtered_links = [string for string in linked_articles if ':' not in string and "/" not in string]

    return filtered_links

# Function to get backlinks from Wikipedia
def get_backlinks(article_title):
    base_url = "https://en.wikipedia.org/w/api.php" # Base URL for Wikipedia API
    params = { # Parameters for the API request
        'action': 'query',
        'format': 'json',
        'list': 'backlinks', 
        'bllimit': 500,  # Maximum number of backlinks 
        'bltitle': article_title, # Title of the page to get backlinks from
    }

    response = requests.get(base_url, params=params) # Send GET request to Wikipedia API
    data = response.json()

    # Extract backlinks from the response
    backlinks = data['query']['backlinks']

    # Filter out backlinks with ":" or "/" in them
    filtered_backlinks = [page['title'] for page in backlinks if ':' not in page['title'] and '/' not in page['title']]

    return filtered_backlinks
    
# Function to count word occurrences in articles
def count_word_occurrences(articles, target_word):
    occurrences_dict = {}
    
    for article_title in articles:
        article_text = get_article_text(article_title) # Get text of the article
        occurrences = article_text.count(target_word) # Count occurrences of target word
        occurrences_dict[article_title] = occurrences
    
    return occurrences_dict

# Function to get the text content of a Wikipedia article
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

        # Extract the page ID of the article. 
        page_id = next(iter(data['query']['pages'].keys()))  #.keys() retrieves the page IDs of the pages dictionary (are the keys), iter() creates iterary, allows us to loop over the key one by one, next() always retrieves the next elment from the iterator 

        # Extract the text content of the article based on the page ID obtained earlier.
        article_text = data['query']['pages'][page_id].get('extract', 'No extract available') #if extract not available it returns: "No extract available"

        return article_text

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Function to get all navbox titles from a Wikipedia article
def get_all_navbox_titles(article_title):
    # Fetch the Wikipedia article content
    url = f"https://en.wikipedia.org/wiki/{article_title}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all navbox sections
    navboxes = soup.find_all("div", {"class": "navbox"})

    # Extract article titles from all navboxes
    titles = []
    for navbox in navboxes:
        for link in navbox.find_all("a", href=re.compile(r"/wiki/")): #Finds all "a" (anchor tags) within navbox section, filter based on the "href" attribute that contains substring "/wiki/"
            title = link.get("title")
            if title:
                titles.append(title)

    return titles

# Function to find duplicate values in a dictionary
def find_duplicate_values(data):
    value_keys = {}  # Dictionary to store keys associated with each value

    # Populate value_keys
    for key, (values, _) in data.items(): #ignore everything except the values
        for value in values:
            if value in value_keys:
                value_keys[value].append(key) #we append the key because we later want to make an edge between the "parent" article
            else:
                value_keys[value] = [key]

    # Filter out duplicates
    duplicate_pairs = {value: keys for value, keys in value_keys.items() if len(keys) > 1} #iterates over each item in value_key.items() (is a tuple) checks if multiple keys are associated with the same value

    return duplicate_pairs
