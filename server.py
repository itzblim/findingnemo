import uri_finder as Finder
from flask import Flask, render_template, request
app = Flask(__name__)

search_term = ""
website_url = ""


@app.route('/')
def popup():
    return render_template('popup.html')


@app.route('/search-link/', methods=['POST'])
def post_search_query():
    global search_term
    if request.method == 'POST':
        search_term = request.get_json()["searchElem"]
        print(search_term)
        return '', 200


@ app.route('/postCurrentUrl-link/', methods=['POST'])
def post_current_url():
    global website_url
    if request.method == 'POST':
        website_url = request.get_json()["currentUrl"]
        print(website_url)
        return '', 200


@ app.route('/getImgUrl-link/', methods=['GET'])
def getImgUrl():
    if request.method == 'GET':
        imgUrls = Finder.generate_imgUrlJS(website_url)
        return imgUrls, 200


if __name__ == '__main__':
    app.run(debug=True)
