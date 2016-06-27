from flask import Flask
from flask import request, render_template
import requests, time, string, re, operator
from lxml import html

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        form_data = request.form['url']
        word_list = check_url(form_data, 5)
        print(word_list)
        return render_template('main.html', slide="url is valid",
                               pos1=word_list[0], pos2=word_list[1], pos3=word_list[2], pos4=word_list[3],
                               pos5=word_list[4], pos6=word_list[5], pos7=word_list[6], pos8=word_list[7],
                               pos9=word_list[8], pos10=word_list[9],neg1=word_list[10], neg2=word_list[11],
                               neg3=word_list[12], neg4=word_list[13], neg5=word_list[14], neg6=word_list[15],
                               neg7=word_list[16], neg8=word_list[17], neg9=word_list[18], neg10=word_list[19],
                               percentage=word_list[20])
    return render_template('main.html', slide="")


# Scrape comments with xpath, find element with data-type comment, then find child with class md and then scrape the
# text within the <p></p> elements
# Strip the comments of all punctuation, separate them by space, lower case all words and split into an array
#
def parse_page(name):
    raw_html = html.fromstring(name.content)
    comments = raw_html.xpath('//div[@data-type="comment"]//div[@class="md"]//text()')
    comment_string = ""
    for comment in comments:
        comment_string += comment
    comment_space_nodot = comment_string.replace(".", " ")
    exclude = set(string.punctuation)
    comments_no_punctuation = ''.join(ch for ch in comment_space_nodot if ch not in exclude)
    comments_nolines = comments_no_punctuation.replace("\n", " ")
    ' '.join(comments_nolines.split())
    string_arr = comments_nolines.split(" ")
    for s in string_arr:
        s.lower()
    return hashmapfunction(string_arr)


def importcsv(filename):
    with open(filename, 'rU') as f:
        wordraw = f.readline()
        words = wordraw.split(",")
        new_dict = {}
        for word in words:
            new_dict[word] = 0
        return new_dict


def hashmapfunction(stringarr):
    positive_hashmap = importcsv('positive-words.csv')
    negative_hashmap = importcsv('negative-words.csv')
    for word in stringarr:
        if word in positive_hashmap.keys():
            positive_hashmap[word] += 1
        elif word in negative_hashmap.keys():
            negative_hashmap[word] += 1
    sorted_positivehashmap = sorted(positive_hashmap.items(), key = operator.itemgetter(1), reverse=True)
    sorted_negativehashmap = sorted(negative_hashmap.items(), key = operator.itemgetter(1), reverse=True)
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
    var = "(https://www.)?reddit.com\/r\/[a-zA-Z_]+\/(comments)\/.*"
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

app.run()
