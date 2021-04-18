from datetime import datetime
import os

import psycopg2
from flask import request, after_this_request


def get_conn():
    return psycopg2.connect(os.environ['DB_CREDENTIALS'])


def get_info(query: str):
    words = query.split(' ')
    clazz1 = '%'
    clazz2 = '%'
    for word in words:
        for ch in word:
            if ch.isdigit():
                if clazz1 != '%':
                    if clazz2 != '%':
                        return ()
                    clazz2 = '%' + word
                else:
                    clazz1 = '%' + word + '%'
                break
    q = ['%', '%', '%']
    if len(words) > 3 and clazz1 == '%' or len(words) > 4 and clazz2 == '%' or len(words) > 5:
        return ()
    else:
        for i in range(len(words)):
            if '%' + words[i] + '%' != clazz1 and '%' + words[i] != clazz2:
                q[i] = '%' + words[i] + '%'
    print('class:', clazz1, clazz2)
    print(q)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from pool where lower(fio) like lower(%s) "
                   "and lower(fio) like lower(%s) and lower(fio) like lower(%s) and clazz like %s and clazz like %s",
                   (q[0], q[1], q[2], clazz1, clazz2))
    ans = cursor.fetchall()
    if len(ans) == 0:
        return None
    return ans


def submit_query(query: str):
    conn = get_conn()
    cursor = conn.cursor()
    time = str(datetime.now())
    cursor.execute("insert into history values (%s, %s)", (query, time))
    conn.commit()


def submit_metric(path: str, data: str, ip: str):
    cookie = request.cookies.get("biscuit")
    conn = get_conn()
    cursor = conn.cursor()
    if cookie is None:
        cursor.execute("select * from cookie_num")
        cookie = cursor.fetchone()[0]+1
        cursor.execute("update cookie_num set num = %s", (cookie,))

        @after_this_request
        def set_cookie(response):
            response.set_cookie('biscuit', cookie)
            return response
    time = str(datetime.now())
    cursor.execute("insert into metric values (%s, %s, %s, %s, %s)", (path, ip, time, data, cookie))
    conn.commit()


def another_one():
    conn = get_conn()
    cursor = conn.cursor()

