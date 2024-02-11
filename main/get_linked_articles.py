import requests

def get_important_links(article_title):
    global important_links
    important_links = []
    linked_articles = get_linked_articles(article_title)
    backlinks = get_backlinks(article_title)

    for element in linked_articles:
        if element in backlinks:
            important_links.append(element)
        
    return important_links


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

        # Extract linked articles
        pages = data['query']['pages'] # accesses values associated to key "query" and then key "pages"
        for page_id in pages:
            page = pages[page_id] # get individual page object
            links = page.get('links', []) # if "links" key is present it returns value associated with it, otherwise the second parameter (empty list)
            linked_articles.extend(link['title'] for link in links) # extend list with titels of the links

       # Check if there are more results
        continue_param = data.get('continue', {}) # retrieves  "continue" parameter from "data" dictoinary (if doesn't exits returns empty dictionary)
        print(continue_param)
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
    return filtered_links

def get_backlinks(article_title):
    print("I get called though?")
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

    print("I mean we do get here right?")
    print("\n\n\n\n\n\n those are the filtered backlinks, ",filtered_backlinks,"\n\n\n\n\n")
    # Calculate the relevance of each linked article
    relevance = {}
    link_titles = []
    for backlink_article in filtered_backlinks:
        relevance_number=0
        print("This article is currently checked, ", backlink_article)
        link_titles.append(get_linked_articles(backlink_article))
        #print("Those are the links of the article, ", link_titles)
        for page in link_titles:
            #page = pages[page_id] # get individual page object
            #links = page.get('links', []) # if "links" key is present it returns value associated with it, otherwise the second parameter (empty list)
            #link_titles.extend(link['title'] for link in links)
            #for link in link_titles:
            if page == article_title:
                relevance_number = relevance_number+1
        relevance[backlink_article]=relevance_number

    print("This is the relevance: ", relevance)

    # Sort linked articles by relevance and retrieve the top 30
    sorted_articles = sorted(relevance.items(), key=lambda x: x[1], reverse=True)
    top_30_articles = [article[0] for article in sorted_articles[:30]]



    return top_30_articles

"""
#Example usage
article_title = "Sursee"
linked_articles = get_linked_articles(article_title)
backlinks = get_backlinks(article_title)
print("Linked Articles: \n\n", linked_articles)
print("Backlinks: \n\n", backlinks)
print("\n\n\n\n Those are the important links: ", important_links)
"""
