from flask import Flask
from flask import request, redirect, render_template
import requests, time, string
import re, csv, operator
from lxml import html

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        form_data = request.form['url']
        arr = check_url(form_data, 5)
        return render_template('main.html', slide="url is valid",
                               pos1=arr[0], pos2=arr[1], pos3=arr[2], pos4=arr[3],
                               pos5=arr[4], pos6=arr[5], pos7=arr[6], pos8=arr[7], pos9=arr[8], pos10=arr[9],
                               neg1=arr[10], neg2=arr[11], neg3=arr[12], neg4=arr[13], neg5=arr[14], neg6=arr[15],
                               neg7=arr[16], neg8=arr[17], neg9=arr[18], neg10=arr[19], percentage=arr[20])
    return render_template('main.html', slide="")

def parse_page(name):
    raw_html = html.fromstring(name.content)
    comments = raw_html.xpath('//div[@data-type="comment"]//div[@class="md"]//text()')
    commentstring = ""
    for comment in comments:
        commentstring += comment
    commentdotnospace = commentstring.replace(".", " ")
    exclude = set(string.punctuation)
    commentsnopunctuation = ''.join(ch for ch in commentdotnospace if ch not in exclude)
    commentsnolines = commentsnopunctuation.replace("\n", " ")
    ' '.join(commentsnolines.split())
    stringarr = commentsnolines.split(" ")
    for s in stringarr:
        s = s.lower()
    return hashmapfunction(stringarr)

def importcsv(filename):
    with open(filename, 'rU') as f:
        wordraw = f.readline()
        words = wordraw.split(",")
        new_dict = {}
        for word in words:
            new_dict[word] = 0
        return new_dict

def hashmapfunction(stringarr):
    positivehashmap = importcsv('positive-words.csv')
    negativehashmap = importcsv('negative-words.csv')
    for word in stringarr:
        if word in positivehashmap.keys():
            positivehashmap[word] += 1
        elif word in negativehashmap.keys():
            negativehashmap[word] += 1
    sorted_positivehashmap = sorted(positivehashmap.items(), key = operator.itemgetter(1), reverse=True)
    sorted_negativehashmap = sorted(negativehashmap.items(), key = operator.itemgetter(1), reverse=True)
    total_positive = total(sorted_positivehashmap)
    total_negative = total(sorted_negativehashmap)
    total_all = total_positive + total_negative
    toptenpos = topten(sorted_positivehashmap)
    toptenneg = topten(sorted_negativehashmap)
    sortedwords = toptenpos + toptenneg
    percentage = (-200 / total_all * total_positive) + 100;
    sortedwords.append(str(round(percentage, 2)))
    return sortedwords


def total(sorted_list):
    i = 0
    total_val = 0
    while i < 10:
        temp_tuple = sorted_list[i]
        total_val += temp_tuple[1]
        i += 1
    return total_val


def topten(arr):
    i = 0
    finalarr = []
    while i < 10:
        if len(arr) > i:
            mypair = arr[i]
            if mypair[1] < 10:
                finalarr.append(" " + str(mypair[1]) + " - " + mypair[0].capitalize())
            else:
                finalarr.append(str(mypair[1]) + " - " + mypair[0].capitalize())
        else:
            finalarr.append("N/A")
        i += 1
    return finalarr


def check_url(url, timeout):
    var = "(https://www.)?reddit.com\/r\/[a-z]+\/(comments)\/.*"
    if re.search(var, url):
        page_name = requests.get(url)
        print(page_name.status_code)
        if page_name.status_code == requests.codes.ok:
            print('website exists ' + url)
            return parse_page(page_name)
        else:
            if timeout > 0:
                print('no website here ' + url + ' trying again...')
                time.sleep(3)
                --timeout
                check_url(url, timeout)
            else:
                print("could not connect")
    else:
        print("no")


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form['url']
    check_url(form_data, 5)
    # return redirect("/")


app.run()
