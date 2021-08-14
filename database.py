from datetime import datetime
import os

import psycopg2
from flask import request, after_this_request, make_response


def get_conn():
    return psycopg2.connect(os.environ['DB_CREDENTIALS'])


full_names = {'саша': 'александр', 'саня': 'александр', 'катя': 'екатерина', 'коля': 'николай',
              'дима': 'дмитрий', 'соня': 'софия', 'оля': 'ольга', 'вова': 'владимир',
              'влад': ['владимир', 'владислав'],
              'настя': 'анастасия', 'ваня': 'иван', 'юра': 'юрий', 'слава': 'вячеслав', 'миша': 'михаил',
              'даня': ['даниил', 'данила'], 'лиза': 'елизавета', 'аня': 'анна', 'рома': 'роман',
              'макс': 'максим', 'гоша': ['георгий', 'григорий'], 'гриша': ['георгий', 'григорий'],
              'паша': 'павел', 'женя': ['евгения', 'евгений'], 'артем': ['артем', 'артём', 'артемий'],
              'тима': 'тимофей', 'сева': 'владислав', 'фёдор': ['фёдор', 'федор'],
              'федор': ['фёдор', 'федор'], 'федя': ['фёдор', 'федор'],
              'света': 'светлана', 'варя': 'варвара', 'ксюша': 'ксения', 'наташа': 'наталья',
              'таня': 'татьяна',
              'тася': 'таисия', 'толя': 'анатолий', 'ира': 'ирина', 'егор': ['георгий', 'егор']}


def get_info(query: str):
    words = query.split(' ')
    clazz1 = '%'
    clazz2 = '%'
    for word in words:
        for ch in word:
            if ch.isdigit():
                if clazz1 == '%':
                    clazz1 = '%' + word + '%'
                else:
                    if clazz2 != '%':
                        return ()
                    clazz2 = '%' + word
                break
    q = ['%', '%', '%']
    if len(words) > 3 and clazz1 == '%' or len(words) > 4 and clazz2 == '%' or len(words) > 5:
        return ()
    else:
        for i in range(len(words)):
            if '%' + words[i] + '%' != clazz1 and '%' + words[i] != clazz2:
                if words[i] in full_names.keys():
                    if isinstance(full_names[words[i]], str):
                        q[i] = '%' + full_names[words[i]] + '%'
                    else:
                        q[i] = '%' + full_names[words[i]][0] + '%'
                else:
                    q[i] = '%' + words[i] + '%'

    print('class:', clazz1, clazz2)
    print(q)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from pool where "
                   "(lower(first_name) like lower(%s) or lower(last_name) like lower(%s)) "
                   "and (lower(first_name) like lower(%s) or lower(last_name) like lower(%s)) "
                   "and (lower(first_name) like lower(%s) or lower(last_name) like lower(%s)) "
                   "and clazz like %s and clazz like %s "
                   "order by (case when vk_id IS NULL then 1 else 0 end), last_name, first_name",
                   (q[0], q[0], q[1], q[1], q[2], q[2], clazz1, clazz2))
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
            response.set_cookie('biscuit', str(cookie))
            return response
    time = str(datetime.now())
    cursor.execute("insert into metric values (%s, %s, %s, %s, %s)", (path, ip, time, data, cookie))
    conn.commit()


def another_one():
    conn = get_conn()
    cursor = conn.cursor()


def get_winners():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from winners")
    return cursor.fetchall()


