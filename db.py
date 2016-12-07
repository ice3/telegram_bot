"""Contains the model for the URL.

Also contains the methods to easily manipulate
"""

import logging
import datetime
from pony import orm
from pony.orm import PrimaryKey, Required, Optional, select, count
import utils

logging.basicConfig(level=logging.WARNING,
                    format=('%(asctime)s - '
                            '%(name)s - '
                            '%(levelname)s - '
                            '%(message)s'
                            ))


db = orm.Database('sqlite', 'url_db.sqlite', create_db=True)


last_sent = None


class Url(db.Entity):
    """Model for the Url."""

    link = PrimaryKey(str)
    priority = Required(int, default=1)  # higher is prioritised
    description = Optional(str)
    created_at = Required(datetime.datetime, sql_default='CURRENT_TIMESTAMP')
    showed_at = Optional(datetime.datetime, 6)
    showed = Required(bool, default=False)
    description = Optional(str)
    category = Optional(str)
    score_like = Required(int, default=0)
    twitted = Required(bool, default=False)
    twitter_description = Optional(str, 140)


orm.sql_debug(True)
db.generate_mapping(create_tables=True)


@orm.db_session
def get_elem(link):
    """Get an element from the database.

    If the element doesn't exists, returns None
    """
    try:
        u = Url[link]
    except:
        logging.error("Error to get element : " + link)
        u = None
    return u


@orm.db_session
def add_url(link):
    """Add an element to the database.

    If the element already exists, doesn't
    add it (or it would cause an error)
    """
    try:
        u = Url[link]
    except:
        u = None
    else:
        logging.warn("Insertion while element already exists : " + link)
    if not u:
        Url(link=link)


@orm.db_session
def add_urls(contexts):
    """Add multiples elements to the dabase.

    This might be more performant (only one transaction, normally)
    """
    [add_url(context) for context in contexts]


@orm.db_session
def change_priority(link, priority):
    """Update the priority for an url.

    If the url doesn't exists it is not modified.
    """
    u = get_elem(link)
    if u:
        u.priority = priority


@orm.db_session
def add_description(link, desc):
    """Add a summary for an url.

    If the url doesn't exists it is not modified.
    """
    u = get_elem(link)
    if u:
        u.description = desc


@orm.db_session
def add_twitter_desc(link, desc):
    """Add a twitter summary for an url.

    If the url doesn't exists it is not modified.
    """
    u = get_elem(link)
    if u:
        u.twitter_description = desc
        if not u.description:
            add_description(link, desc)


@orm.db_session
def change_notation(link, note):
    """Change the note for an url.

    If the url doesn't exists it is not modified.
    """
    u = get_elem(link)
    if u:
        u.note = note


@orm.db_session
def get_url_to_show():
    """Return a new link to read.

    If all the database items are read, returns None
    """
    req = (u for u in Url if not u.showed)
    res = select(req).order_by(Url.priority.desc()).limit(1)
    if not res:
        return None
    return res[0].link


@orm.db_session
def url_showed_today():
    """Tell how many links we got today."""
    today = datetime.datetime.today().date()
    return count((u for u in Url if u.showed_at.date() == today))


@orm.db_session
def show(link):
    """Update an item in the database to say it is sent.

    If the url doesn't exists it is not modified.
    """
    global last_sent
    u = get_elem(link)
    last_sent = u
    if u:
        u.showed = True
        u.showed_at = datetime.datetime.utcnow()


@orm.db_session
def tweeted(link):
    """Tweet an Url.

    If the url doesn't exists it is not modified.
    """
    u = get_elem(link)
    if u:
        print("tweeted")
        u.tweeted = True


@orm.db_session
def main(filename):
    """Add."""
    urls = utils.extract_urls_from_text(open(filename).read())
    urls = ({"link": l} for l in urls)
    with orm.db_session:
        add_urls(urls)


def tmp():
    """Plop."""
    with orm.db_session:
        u = get_url_to_show()
        if u:
            print(u)
            show(u)
            print(url_showed_today())
            tweeted(u)
        else:
            print("Nothing to show")


if __name__ == '__main__':
    main("./links.txt")
