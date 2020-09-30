from flask import Flask, request, render_template
from database import get_info, submit_query

app = Flask(__name__)


# todo доработать поиск (саня -> Александр; 11 1)
# todo доработать майнер вк (понять, почему не все из нашего класса)
# todo добавить placeholder (например, Эля 11)


@app.route('/')
def root():
    return render_template('google.html')


@app.route('/redirect')
def rickroll():
    return '<head>\
<meta http-equiv="refresh" content="1;URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" /></head>'


@app.route('/search')
def search():
    query = request.args.get('q', '')
    submit_query(query)
    info = get_info(query)
    return render_template('info.html', info=info)


@app.route('/db')
def db():
    query = request.args.get('name', '')
    return str(get_info(query))

