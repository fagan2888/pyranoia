from requests_html import HTMLSession
from utils import DBConnection
from datetime import datetime

session = HTMLSession()
db = DBConnection('infowars')
today = datetime.today().strftime('%Y-%m-%d')

url = 'https://www.infowars.com'
r = session.get(url)

category_elements_selector = '#menu-item-216953 > ul > li > a'
article_elements_selector = 'article > div > h3 > a'
paragraph_elements_selector = 'article > p'
date_selector = 'span.date'

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
    article_links[category] = [element.attrs['href']
            for element in article_elements]
    db.add_entries_to_table(
        [[category, today, article_name]
            for article_name in article_links[category]],
        'categorized_articles'
    )

text_content = {}
for category, articles in article_links.items():
    for article in articles:
        r_article = session.get(article)
        paragraph_elements = r_article.html.find(selector=paragraph_elements_selector)
        text_content[article] = [paragraph.text for paragraph in paragraph_elements]
        publish_date = r_article.html.find(selector=date_selector, first=True).text
        publish_date = datetime.strptime(publish_date, '%B %d, %Y').strftime('%Y-%m-%d')
        db.add_entries_to_table(
            [[article, publish_date, today,  ' '.join(text_content[article])]],
            'article_content'
        )


