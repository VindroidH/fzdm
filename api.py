import fzdm
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!!!'
    
@app.route('/list')
def get_list():
    list = fzdm.getComics()
    return list