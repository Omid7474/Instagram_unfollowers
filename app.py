from flask import Flask, render_template
import webbrowser
import json
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_data_from_html():
    # Read the followers and following HTML files
    with open("followers_1.html", "r", encoding="utf-8") as followers_file:
        followers_html = followers_file.read()

    with open("following.html", "r", encoding="utf-8") as following_file:
        following_html = following_file.read()

    # Parse HTML
    followers_soup = BeautifulSoup(followers_html, "html.parser")
    following_soup = BeautifulSoup(following_html, "html.parser")

    # Extract usernames from followers
    followers = [a.text for a in followers_soup.find_all("a", href=True)]

    # Extract usernames from following
    following = [a.text for a in following_soup.find_all("a", href=True)]

    return followers, following

def extract_data_from_json():
    # Read the followers and following JSON files
    with open("followers_1.json", "r", encoding="utf-8") as followers_file:
        followers_data = json.load(followers_file)
    
    with open("following.json", "r", encoding="utf-8") as following_file:
        following_data = json.load(following_file)

    # Extract usernames from JSON
    followers = [user['username'] for user in followers_data['followers']]
    following = [user['username'] for user in following_data['following']]

    return followers, following

def extract_data():
    # Check if input files are HTML or JSON
    if os.path.exists("followers_1.html") and os.path.exists("following.html"):
        followers, following = extract_data_from_html()
    elif os.path.exists("followers_1.json") and os.path.exists("following.json"):
        followers, following = extract_data_from_json()
    else:
        raise FileNotFoundError("Input files not found. Ensure either HTML or JSON files are present.")

    # Find following who are not followers
    not_following_back = [user for user in following if user not in followers]

    # Generate list with URLs of people not followed back (for HTML input)
    if os.path.exists("following.html"):
        following_html = open("following.html", "r", encoding="utf-8").read()
        following_soup = BeautifulSoup(following_html, "html.parser")
        not_following_back_urls = [a['href'] for a in following_soup.find_all("a", href=True) if a.text in not_following_back]
    else:
        # Placeholder URLs for JSON input (if URLs are not provided in JSON)
        not_following_back_urls = [f"https://instagram.com/{user}" for user in not_following_back]

    return not_following_back, not_following_back_urls

@app.route('/')
def index():
    try:
        # Extract data from HTML or JSON files
        not_following_back, not_following_back_urls = extract_data()

        # Zip the lists of users and URLs
        data = list(zip(not_following_back, not_following_back_urls))

        # Pass the zipped data to the template
        return render_template('index.html', data=data)
    except FileNotFoundError as e:
        return str(e)

if __name__ == '__main__':
    # Open the URL automatically in the default browser
    webbrowser.open('http://127.0.0.1:5000')

    # Run the Flask app
    app.run(debug=True)
