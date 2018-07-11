from requests_html import HTMLSession

session = HTMLSession()

url = 'https://www.infowars.com'
r = session.get(url)

category_elements_selector = '#menu-item-216953 > ul > li > a'
article_elements_selector = 'article > div > h3 > a'
paragraph_elements_selector = 'article > p'

# get the categories
category_elements = r.html.find(category_elements_selector)
categories = [category.attrs['href'] for category in category_elements]

# consolidate pages to look at for articles
categories.append(url)

# get article links
article_links = {}
for category in categories: 
    r_category = session.get(category)
    article_elements = r.html.find(article_elements_selector)
    article_links[category] = [element.attrs['href'] for element in article_elements]

text_content = {}
for category, articles in article_links.items():
    for article in articles:
        r_article = session.get(article)
        paragraph_elements = r_article.html.find(selector=paragraph_elements_selector)
        text_content[article] = [paragraph.text for paragraph in paragraph_elements]




