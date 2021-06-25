import uri_finder as Finder
from flask import Flask, render_template, request
app = Flask(__name__)

search_term = ""
website_url = ""


@app.route('/')
def popup():
    return render_template('popup.html')


@app.route('/search-link/', methods=['POST'])
def get_search_query():
    if request.method == 'POST':
        search_term = request.get_json()["searchElem"]
        print(search_term)
        return '', 200


@ app.route('/currentUrl-link/', methods=['POST'])
def get_current_url():
    if request.method == 'POST':
        website_url = request.get_json()["currentUrl"]
        print(website_url)
        Finder.generate_imgUrlJS(website_url)
        # Some File Closed IO Error here
        # Only works 1st time when loading server
        return '', 200


if __name__ == '__main__':
    app.run(debug=True)
