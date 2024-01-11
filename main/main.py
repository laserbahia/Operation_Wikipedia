import requests

def get_linked_articles(article_title):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'titles': article_title,
        'prop': 'links',
        'format': 'json'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract linked articles
    linked_articles = []
    pages = data['query']['pages']
    for page_id in pages:
        links = pages[page_id].get('links', [])
        linked_articles.extend(link['title'] for link in links)

    return linked_articles

#Example usage
article_title = "Python (programming language)"
linked_articles = get_linked_articles(article_title)
print("Linked Articles:", linked_articles)