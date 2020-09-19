from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<head>\
<meta http-equiv="refresh" content="1;URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ" />\
</head>'
