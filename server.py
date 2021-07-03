import uri_finder as Finder
from flask import Flask, render_template, request
import json
import main as Backend
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

app = Flask(__name__)

search_term = ""
website_url = ""
images_matched = []
current_match = 0

img_data = 0

@app.route('/')
def popup():
    return render_template('popup.html')


@app.route('/search-link/', methods=['POST'])
def post_search_query():
    global search_term
    global images_matched
    if request.method == 'POST':
        search_term = request.get_json()["searchElem"]
        print("Query: "+ search_term + " sent to server.py")
        images_matched = Backend.find(img_data, search_term)
        print("Images from query highlighted.")
        return '', 200


@app.route('/postCurrentUrl-link/', methods=['POST'])
def post_current_url():
    global website_url
    global img_data
    if request.method == 'POST':
        website_url = request.get_json()["currentUrl"]
        print("Load request: " + website_url + " sent to server.py.")
        img_data = Backend.load_url(website_url)
        print("Website loaded.")
        return '', 200

@app.route('/getImgUrl-link/', methods=['GET'])
def getImgUrl():
    if request.method == 'GET':
        url_mapping = img_data[0] + img_data[2]
        return json.dumps(url_mapping), 200

@app.route('/getImgsMatched/', methods=['GET'])
def getImgsMatched():
    if request.method == 'GET':
        return json.dumps(images_matched), 200

def start_server():
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target = start_server)
    t.start()
    app.run(debug=False)
    

    

    
