import requests



def get_linked_articles(article_title):
    base_url = "https://en.wikipedia.org/w/api.php" #url for the api
    params = { # define parameters in api request
        'action': 'query', # query action, so retrieving information
        'titles': article_title, # information that is request
        'prop': 'links', # property of the page to retrieve information from
        'format': 'json' # response format
    }

    response = requests.get(base_url, params=params) # get request
    data = response.json()

    # Extract linked articles
    linked_articles = []
    pages = data['query']['pages'] # accesses values associated to key "query" and then key "pages"
    for page_id in pages:
        links = pages[page_id].get('links', []) # if "links" key is present it returns value associated with it, otherwise the second parameter (empty list)
        linked_articles.extend(link['title'] for link in links) # extend list with titels of the links

    return linked_articles


#Example usage
article_title = "Python"
linked_articles = get_linked_articles(article_title)
print("Linked Articles:", linked_articles)


