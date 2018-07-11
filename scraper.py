from requests_html import HTMLSession

session = HTMLSession()

r = session.get('https://www.infowars.com')

article_elements = r.html.find('article > div > h3 > a')

article_urls = [element.attrs['href'] for element in article_elements]
text_content = {}
for article in article_urls:
    r_article = session.get(article)
    paragraph_elements = r_article.html.find(selector='article > p')
    text_content[article] = [paragraph.text
                                for paragraph in paragraph_elements]


print(article_urls)
print(text_content)
