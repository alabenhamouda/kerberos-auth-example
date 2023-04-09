#!/usr/bin/env python

from flask import Flask, request
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication
import helpers
import os

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
@requires_authentication
def index(user):
    return f"Authentication successfull, mister {user}"


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


@app.route('/read_file', methods=['POST'])
@requires_authentication
def read_file(principal):
    user = helpers.unix_user(principal)
    home = helpers.get_user_home_dir(user)
    # Get the file path from the request form
    file_path = request.form.get('file_path')
    if file_path:
        file_path = home + file_path
        print(file_path)
        try:
            # Open the file in text mode for reading
            with open(file_path, 'r') as file:
                # Read the file contents as text
                file_contents = file.read()
                # Return the file contents as the response
                return file_contents
        except FileNotFoundError:
            return 'File not found', 404
    else:
        return 'File path parameter is missing', 400


@app.route('/directory', methods=['POST'])
@requires_authentication
def directory_content(principal):
    user = helpers.unix_user(principal)
    home = helpers.get_user_home_dir(user)
    path = request.form.get('path')
    path = home + path
    try:
        # check if it is a file
        if os.path.isfile(path):
            return "This path points to a file", 200
        # if it's not a file, assume it's a directory
        else:
            # get the content of the directory
            content = os.listdir(path)
            return '\n'.join(content), 200
    except FileNotFoundError:
        return "Directory not foudn!", 404
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    init_kerberos(app, service="host")
    app.run(host='0.0.0.0')
