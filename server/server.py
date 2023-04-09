#!/usr/bin/env python

from flask import Flask, request
from flask import render_template
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication

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
def upload_file(user):
    print(user)
    file = request.files['file']
    print(file)
    file.save('/home/kali/uploads/' + file.filename)
    return 'File uploaded!', 200

if __name__ == '__main__':
    init_kerberos(app, service="host")
    app.run(host='0.0.0.0')
