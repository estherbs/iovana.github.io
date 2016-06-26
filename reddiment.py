from flask import Flask
from flask import request, redirect, render_template
import requests, time, string
import re
from lxml import html

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        form_data = request.form['url']
        check_url(form_data, 5)
        return render_template('main.html', slide="url is valid")
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
    print(stringarr)
    return 0


def check_url(url, timeout):
    var = "(https://www.)?reddit.com\/r\/[a-z]+\/(comments)\/.*"
    if re.search(var, url):
        page_name = requests.get(url)
        print(page_name.status_code)
        if page_name.status_code == requests.codes.ok:
            print('website exists ' + url)
            parse_page(page_name)
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
