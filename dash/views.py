from flask import Flask, render_template

from config import client_id, secret, hackathon_name

import urllib, json

dash = Flask(__name__)
url = ""
data = []


@dash.route('/')
def index():
    return render_template('index.html', data=data, hackathon_name=hackathon_name)

@dash.route('/sorted_univ', strict_slashes=False)
def sort_univ():
    return render_template('index.html', data=sorted(data, key=lambda x: x["school"]["name"]), hackathon_name=hackathon_name)

@dash.route('/sorted_name', strict_slashes=False)
def sort_name():
    return render_template('index.html', data=sorted(data, key=lambda x: x["first_name"].lower() + " " + x["last_name"].lower()), hackathon_name=hackathon_name)

@dash.route('/sorted_gender', strict_slashes=False)
def sort_gender():
    return render_template('index.html', data=sorted(data, key=lambda x: x["gender"]), hackathon_name=hackathon_name)

if __name__ == '__main__':
    url = "https://my.mlh.io/api/v1/users?client_id={0}&secret={1}".format(client_id, secret)
    response = urllib.urlopen(url)
    data = json.loads(response.read())["data"]

    dash.run()
