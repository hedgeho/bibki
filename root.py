from flask import Flask, request
from database import get_info
app = Flask(__name__)


@app.route('/')
def root():
    return ''


@app.route('/redirect')
def rickroll():
    return '<head>\
<meta http-equiv="refresh" content="1;URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" /></head>'


@app.route('/db')
def db():
    query = request.args.get('name', '')
    return str(get_info(query))

