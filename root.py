from flask import Flask, request, render_template
from database import get_info
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('google.html')


@app.route('/redirect')
def rickroll():
    return '<head>\
<meta http-equiv="refresh" content="1;URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" /></head>'


@app.route('/db')
def db():
    query = request.args.get('name', '')
    return str(get_info(query))

