from sqlite3 import connect, IntegrityError
from logbook import Logger
from constants import create_table

log_channel_name = 'scrape'
log = Logger(log_channel_name)

class DBConnection(object):

    def __init__(self, db_name):
        self._db = db_name

    def _ensure_table_exists(self, conn, table_name):
        result = conn.execute(
            "SELECT * from sqlite_master WHERE type='table' AND name=?;",
            (table_name,)
        ).fetchall()
        if len(result) == 1:
            return
        elif len(result) > 1:
            raise ValueError(
                "There are multiple {0} tables!".format(table_name)
            )
        log.info("Creating table {0}".format(table_name))
        conn.execute(create_table[table_name])
        conn.commit()

    def add_entries_to_table(self, new_entries, table_name):
        if len(new_entries) == 0:
            return
        command = "INSERT INTO {0} VALUES({1});".format(
            table_name,
            ','.join('?'*len(new_entries[0]))
        )
        log.info(
            'Adding {num} entries to table {table}.',
            num=len(new_entries),
            table=table_name
        )
        with connect(self._db) as conn:
            self._ensure_table_exists(conn, table_name)
            for entry in new_entries:
                try:
                    conn.execute(command, entry)
                    log.info('New entry: {0}'.format(entry))
                except IntegrityError:
                    log.debug('Entry already exists: {0}'.format(entry))
            conn.commit()
    
    def fetch_article_content(self, date=None, category=None):
        if not date:
            date = '2000-01-01'
        if category:
            return self._fetch_article_content_by_category(
                date,
                category
            )
        else:
            return self._fetch_all_articles(date)


    def _fetch_article_content_by_category(self, date, category=None):
        with connect(self._db) as conn:
            result = conn.execute(
                ("""
                    SELECT article_name, content
                    FROM article_content 
                    JOIN categorized_articles
                    ON article_content.article_name = categorized_articles.article_name
                    WHERE categorized_articles.category_name = ?
                    AND article_content.publish_date >= ?;
                """),
                (category, date)
            ).fetchall()
        return result

    def _fetch_all_articles(self, date):
        with connect(self._db) as conn:
            result = conn.execute(
                ("""
                    SELECT article_name, content
                    FROM article_content
                    WHERE article_content.publish_date >= ?;
                """),
                (date,)
            ).fetchall()
        return result
