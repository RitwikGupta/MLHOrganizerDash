from flask import Flask, render_template

from config import client_id, secret, hackathon_name

import urllib, json

dash = Flask(__name__)
url = ""
data = []


@dash.route('/')
def index():
    return render_template('index.html', data=data, hackathon_name=hackathon_name)

@dash.route('/stats', strict_slashes=False)
def stats():

    from collections import defaultdict

    stats = {
        "gender": defaultdict(int),
        "university": defaultdict(int)
    }

    for person in data:
        stats["gender"][person["gender"].lower()] += 1
        stats["university"][person["school"]["name"]] += 1

    stats["gender"] = dict(stats["gender"])
    stats["university"] = sorted(stats["university"].iteritems(), key=lambda x: x[1], reverse=True)

    return render_template('stats.html', data=data, stats=stats)

if __name__ == '__main__':
    url = "https://my.mlh.io/api/v1/users?client_id={0}&secret={1}".format(client_id, secret)
    response = urllib.urlopen(url)
    data = json.loads(response.read())["data"]

    dash.run(debug=True)
