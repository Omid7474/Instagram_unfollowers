from flask import Flask, render_template
from bs4 import BeautifulSoup
import webbrowser

app = Flask(__name__)

# Function to parse HTML files and extract data
def extract_data():
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

    # Find following who are not followers
    not_following_back = [user for user in following if user not in followers]

    # Generate list with URLs of people not followed back
    not_following_back_urls = [a['href'] for a in following_soup.find_all("a", href=True, text=not_following_back)]

    return not_following_back, not_following_back_urls

@app.route('/')
def index():
    # Extract data from HTML files
    not_following_back, not_following_back_urls = extract_data()

    # Zip the lists of users and URLs
    data = list(zip(not_following_back, not_following_back_urls))

    # Pass the zipped data and the enumerate function to the template
    return render_template('index.html', data=data, enumerate=enumerate)

if __name__ == '__main__':
    # Open the URL automatically in the default browser
    webbrowser.open('http://127.0.0.1:5000')

    # Run the Flask app
    app.run(debug=True)
