"""
import requests

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
    linked_articles = []

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

        
       

    return linked_articles

#Example usage
article_title = "Switzerland"
linked_articles = get_linked_articles(article_title)
print("Linked Articles:", linked_articles)
"""



import requests

def get_linked_articles(article_title):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'titles': article_title,
        'prop': 'links',
        'format': 'json',
        'pllimit': 500,
        'plnamespace': 0, # filter by main namespace
        'plgenerator': 'allpages',
        'gaplimit': 500,
    }

    linked_articles = []
    page_ids = {}

   

    while True:
        response = requests.get(base_url, params=params) # get request
        data = response.json()
        # Extract linked articles
        pages = data['query']['pages'] # accesses values associated to key "query" and then key "pages"
        for page_id in pages:
            page = pages[page_id] # get individual page object
            links = page.get('links', []) # if "links" key is present it returns value associated with it, otherwise the second parameter (empty list)
            linked_articles.extend(link['title'] for link in links) # extend list with titels of the links
            for link in links:
                page_ids[link['title']] = int(page_id)

       # Check if there are more results
        continue_param = data.get('continue', {}) # retrieves  "continue" parameter from "data" dictoinary (if doesn't exits returns empty dictionary)
        print(continue_param)
        if not continue_param: # checks if contine_param is an empty list
            break

        # Update the params with the continue parameter
        params.update(continue_param)

    print("Those are the linked articles:",linked_articles)

    # Calculate the relevance of each linked article
    relevance = {}
    link_titles = []
    for article in linked_articles:
        params['titles']=article # updating the parameters to the current article 
        relevance_number=0
        link_titles=[]
        response = requests.get(base_url, params=params) # get request
        data = response.json()
        pages = data['query']['pages'] # accesses values associated to key "query" and then key "pages"
        for page_id in pages:
            page = pages[page_id] # get individual page object
            links = page.get('links', []) # if "links" key is present it returns value associated with it, otherwise the second parameter (empty list)
            link_titles.extend(link['title'] for link in links)
            for link in link_titles:
                if link == "Sursee":
                    relevance_number = relevance_number+1
        relevance[article]=relevance_number

    print("This is the relevance: ", relevance)

    # Sort linked articles by relevance and retrieve the top 30
    sorted_articles = sorted(relevance.items(), key=lambda x: x[1], reverse=True)
    top_30_articles = [article[0] for article in sorted_articles[:30]]

    return top_30_articles

#Example usage
article_title = "Sursee"
main_article_title = article_title
top_30_articles = get_linked_articles(article_title)
print("Top 30 Linked Articles:", top_30_articles)



