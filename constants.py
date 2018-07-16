
create_table = {
    'article_content': '''
        CREATE TABLE article_content
        (
            article_name TEXT NOT NULL,
            publish_date DATE NOT NULL,
            scrape_date DATE NOT NULL,
            content TEXT
        );
    ''',
    'categorized_articles': '''
        CREATE TABLE categorized_articles
        (
            category_name TEXT NOT NULL,
            scrape_date DATE NOT NULL,
            article_name TEXT NOT NULL
        );
    '''
}

