#!/usr/bin/env python3

import os
import json
import datetime as dt

from flask import Flask, abort, render_template, request, jsonify

from ivoc.parser import prepare

app = Flask('ivoc')

@app.route('/')
def index():
    return f'Test'

@app.route('/text/<text_name>')
def text(text_name):
    if not os.path.exists('%s.txt' % text_name):
        abort(404)

    with open('%s.txt' % text_name, 'rt') as f:
        data = f.read()

    with open('db.json', 'rt') as f:
        d = json.loads(f.read())

    return render_template('text.html', title=text_name, contents=prepare(data, d))

def update_database(word, status, source):
    with open('db.json', 'rt') as f:
        d = json.loads(f.read())

    if word in d.keys():
        d[word]['status'] = status
    else:
        d[word] = {'added': date = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
                   'status': status,
                   'source': source}

    with open('db.json', 'wt') as f:
        f.write(json.dumps(db, indent=4, sort_keys=True, ensure_ascii=False))

@app.route('/api/update', methods=['POST'])
def api_update():
    data = request.get_json()
    print(data)
    return jsonify({"status": "OK"})
