from flask import Flask
from flask import request, redirect, render_template
import requests, time
import re

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        form_data = request.form['url']
        checkurl(form_data, 5)
        return render_template('main.html', slide="url is valid")
    return render_template('main.html', slide="")


def parsepage(name):
    return 0

def checkurl(url, timeout):
    var = "(https://www.)?reddit.com\/r\/[a-z]+\/(comments)\/.*"
    if re.search(var, url):
        page_name = requests.get(url)
        print(page_name.status_code)
        if page_name.status_code == requests.codes.ok:
            print('website exists ' + url)
            parsepage(page_name)
        else:
            if(timeout > 0):
                print('no website here ' + url + ' trying again...')
                time.sleep(3)
                --timeout
                checkurl(url, timeout)
            else:
                print("could not connect")
    else:
        print("no")



@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form['url']
    checkurl(form_data, 5)
    # return redirect("/")


app.run()
