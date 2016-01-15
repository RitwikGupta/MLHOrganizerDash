from flask import Flask, render_template, redirect, url_for, send_file

from config import client_id, secret, hackathon_name

import urllib, json
import datetime
import random
import matplotlib.pyplot as plt
import StringIO

from collections import defaultdict

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
        "university": defaultdict(int),
        "diet_rest": defaultdict(int)
    }

    for person in data:
        stats["gender"][person["gender"].lower()] += 1
        stats["university"][person["school"]["name"].lower().strip()] += 1
        stats["diet_rest"][person["dietary_restrictions"]] += 1

    stats["gender"] = dict(stats["gender"])
    stats["university"] = sorted(stats["university"].iteritems(), key=lambda x: x[1], reverse=True)
    stats["university"] = map(lambda x: (x[0].lower().strip(), x[1]), stats["university"])

    stats["diet_rest"] = sorted(stats["diet_rest"].iteritems(), key=lambda x: x[1], reverse=True)
    stats["diet_rest"] = map(lambda x: (x[0].lower().strip(), x[1]), stats["diet_rest"])

    med = median(list(set(map(lambda x: x[1], stats["university"])))) # Lol

    return render_template('stats.html', data=data, stats=stats, median=med, hackathon_name=hackathon_name)

@dash.route('/refresh', strict_slashes=False)
def refresh():
    global data

    url = "https://my.mlh.io/api/v1/users?client_id={0}&secret={1}".format(client_id, secret)
    response = urllib.urlopen(url)
    data = json.loads(response.read())["data"]

    return redirect('/')

@dash.route('/getgraphs', strict_slashes=False)
def getgraphs():
    return send_file(makeGraphs(), mimetype='image/png')

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
        return None
    if len(lst) %2 == 1:
        return lst[((len(lst)+1)/2)-1]
    else:
        return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

def makeGraphs():
    t_x = map(lambda x: (x["updated_at"], 1), data)

    date_count = defaultdict(int)

    for date, num in t_x:
        date_count[datetime.datetime.strptime(date[:10],'%Y-%m-%d')] += 1

    t_x = dict(date_count)

    t_x = t_x.items()
    t_x.sort()
    t_x = t_x[1:]

    x = map(lambda x: x[0], t_x)
    y = map(lambda y: y[1], t_x)

    e_y = [sum(y[:i+1]) for i in range(len(y))]


    f, (p1, p2) = plt.subplots(1, 2, sharey=False)
    p1.plot(x, y)
    p1.set_title("Number of registrants per day for SteelHacks")
    p1.set_ylabel("Number of registrants per day")
    p1.set_xlabel("Days")

    p2.plot(x, e_y)
    p2.set_title("Total number of registrations over time for SteelHacks")
    p2.set_ylabel("Number of registrants total")
    p2.set_xlabel("Days")

    img = StringIO.StringIO()
    f.savefig(img)
    img.seek(0)

    return img

if __name__ == '__main__':
    url = "https://my.mlh.io/api/v1/users?client_id={0}&secret={1}".format(client_id, secret)
    response = urllib.urlopen(url)
    data = json.loads(response.read())["data"]

    dash.run(debug=True)
