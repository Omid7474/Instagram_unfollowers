from flask import Flask, render_template
import webbrowser
from extractJson import jsonExt
from extractHtml import htmlExt

app = Flask(__name__)

# Function to parse JSON if there are JSON files, otherwise HTML files, and extract data
def extract_data():
    try:
        # Try to extract data from JSON files
        not_following_back, not_following_back_urls = jsonExt("followers_1.json", "following.json")
    except FileNotFoundError:
        # If JSON files are not found, extract data from HTML files
        not_following_back, not_following_back_urls = htmlExt("followers_1.html", "following.html")

    return not_following_back, not_following_back_urls

@app.route('/')
def index():
    not_following_back, not_following_back_urls = extract_data()
    data = list(zip(not_following_back, not_following_back_urls))
    return render_template('index.html', data=data, enumerate=enumerate)

if __name__ == '__main__':
    # Open the URL automatically in the default browser
    webbrowser.open('http://127.0.0.1:5000')

    # Run the Flask app
    app.run()
