import psycopg2


def get_conn():
    return psycopg2.connect(***REMOVED***
     ***REMOVED***)


def get_info(query):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from pool where last_name=%s", (query,))
    return cursor.fetchall()
