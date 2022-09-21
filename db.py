import psycopg2 as psyco
import urllib.parse as up

def connect_db():
    """Establish connection to db"""
    conn = None
    try:
        up.uses_netloc.append("postgres")
        url = up.urlparse('the url is being removed due to privacy issue')
        conn = psyco.connect(database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except (Exception, psyco.DatabaseError) as e:
        print(e)
    finally:
        return conn
