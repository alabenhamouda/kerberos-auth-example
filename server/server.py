#!/usr/bin/env python

from flask import Flask, request
from flask import render_template
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication
import helpers

DEBUG=True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
@requires_authentication
def index(user):
    return render_template('index.html', user=user)

@app.route("/test")
def test():
    return render_template('index.html', user="non authenticated")

@app.route('/upload', methods=['POST'])
@requires_authentication
def upload_file(principal):
    user = helpers.unix_user(principal) 
    file = request.files['file']
    dest_path = request.form.get('dest_path')
    if not dest_path.endswith("/") and dest_path != "":
        dest_path = dest_path + "/"
    file.save(helpers.get_user_home_dir(user) + dest_path + file.filename)
    return 'File uploaded!', 200

if __name__ == '__main__':
    init_kerberos(app, service="host")
    app.run(host='0.0.0.0')
