from flask import Flask, render_template, redirect, url_for, send_file, make_response

from config import client_id, secret, hackathon_name

import urllib, json
import datetime
import random
import os 

import matplotlib.pyplot as plt
import tempfile
import matplotlib
matplotlib.use('Agg') # this allo

from collections import defaultdict

dash = Flask(__name__, static_url_path='')

url = ""
data = []


@dash.route('/')
def index():
    return render_template('index.html', data=data, hackathon_name=hackathon_name)

@dash.route('/stats', strict_slashes=False)
def stats():

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

    try:
        os.remove('dash/static/img/graph.png')
        os.remove('dash/static/img/graphTwo.png')
    except OSError:
        pass

    f = open('dash/static/img/graph.png', 'w')
    plt.plot(x,y)
    plt.ylabel("Number of registrants per day")
    plt.xlabel("Days")
    plt.title("Number of registrants per day for SteelHacks")
    plt.savefig(f)
    f.close() # close the file

    plt.clf()

    f = open('dash/static/img/graphTwo.png', 'w')
    plt.plot(x, e_y)
    plt.ylabel("Number of registrants total")
    plt.xlabel("Days")
    plt.title("Total number of registrations over time for SteelHacks")
    plt.savefig(f)
    f.close()

    plt.clf()

    return render_template('stats.html', data=data, stats=stats, median=med, hackathon_name=hackathon_name)

@dash.route('/refresh', strict_slashes=False)
def refresh():
    global data

    url = "https://my.mlh.io/api/v1/users?client_id={0}&secret={1}".format(client_id, secret)
    response = urllib.urlopen(url)
    data = json.loads(response.read())["data"]

    return redirect('/')

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
        return None
    if len(lst) %2 == 1:
        return lst[((len(lst)+1)/2)-1]
    else:
        return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

#@dash.route('/getgraphs', strict_slashes=False)
#def getgraphs():

  
#    canvas=FigureCanvas(f)
#    png_output = StringIO.StringIO()
#    canvas.print_png(png_output)
#    response=make_response(png_output.getvalue())
#    response.headers['Content-Type'] = 'image/png'
#    return response
    
if __name__ == '__main__':
    url = "https://my.mlh.io/api/v1/users?client_id={0}&secret={1}".format(client_id, secret)
    response = urllib.urlopen(url)
    data = json.loads(response.read())["data"]

    dash.run(debug=True)
