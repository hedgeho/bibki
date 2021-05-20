from flask import Flask, request, render_template, abort, url_for, redirect

from database import get_info, submit_query, submit_metric, get_winners
from methods import calculate_math

app = Flask(__name__)


# todo доработать поиск
# todo доработать майнер вк
# to.done? добавить placeholder (например, Эля 11)
# todo цитаты мса
# todo счетчик рикроллов


@app.route('/')
def root():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/', '', request.environ['HTTP_X_FORWARDED_FOR'])
    return render_template('google.html', matesha=calculate_math())


@app.route('/monke')
def monke():
    return render_template('monke.html')


@app.route('/redirect')
def rickroll():
    return '<head>' \
           '<meta http-equiv="refresh" content="1;URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" /></head>'


@app.route('/p')
def presentation():
    return '<head><meta http-equiv="refresh" ' \
           'content="1;' \
           'URL=https://docs.google.com/presentation/d/1QRdGjsjxfOrV-vojznz5S79UQO1hDbysoZme2Cgyh2o/edit?usp=sharing' \
           '?usp=sharing" /></head> '


@app.route('/search')
def search():
    query = request.args.get('q', '')
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/search', query, request.environ['HTTP_X_FORWARDED_FOR'])
    info = get_info(query)
    return render_template('info.html', info=info, query=query)


@app.route('/db')
def db():
    query = request.args.get('name', '')
    return str(get_info(query))


# event 21/05
@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/check')
def check():
    number = int(request.args.get('number', ''))
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/', str(number), request.environ['HTTP_X_FORWARDED_FOR'])

    winners = get_winners()
    print(winners)
    if len(winners) == 0:
        return redirect(url_for('wait'))
    elif (number,) in winners:
        return redirect(url_for('win'))
    else:
        return redirect(url_for('lose'))


@app.route('/wait')
def wait():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/', '', request.environ['HTTP_X_FORWARDED_FOR'])
    return render_template('wait.html')


@app.route('/lose')
def lose():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/', '', request.environ['HTTP_X_FORWARDED_FOR'])
    return render_template('lose.html')


@app.route('/win')
def win():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        submit_metric('/', '', request.environ['HTTP_X_FORWARDED_FOR'])
    return render_template('win.html')

