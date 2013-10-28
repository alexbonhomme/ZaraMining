'''
Created on 26 oct. 2013

@author: Alexandre Bonhomme
'''
from flask import Flask, json
from fr.blckshrk.zaramining.main import Main
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/api/<lang>/<section>/<subsection>/')
def api(lang, section, subsection):
    bot = Main(lang, section, subsection)

    return json.dumps({'meta': {'lang': lang},
                       'content': bot.run()},
                       sort_keys = False)

if __name__ == '__main__':
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
