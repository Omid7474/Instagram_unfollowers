from bs4 import BeautifulSoup

def htmlExt(followers_html_path='followers_1.html', following_html_path='following.html'):
    """
    Extracts usernames and profile URLs from followers and following HTML files.

    :param followers_html_path: Path to the followers HTML file
    :param following_html_path: Path to the following HTML file
    :return: Two lists - not_following_back and not_following_back_urls
    """
    # Read HTML files
    with open(followers_html_path, 'r', encoding='utf-8') as file:
        followers_html = file.read()
    
    with open(following_html_path, 'r', encoding='utf-8') as file:
        following_html = file.read()

    # Parse HTML content with BeautifulSoup
    followers_soup = BeautifulSoup(followers_html, 'html.parser')
    following_soup = BeautifulSoup(following_html, 'html.parser')
    
    # Extract followers usernames and URLs
    followers = {a.text: a['href'] for a in followers_soup.find_all('a', href=True)}

    # Extract following usernames and URLs
    following = {a.text: a['href'] for a in following_soup.find_all('a', href=True)}

    # Identify not-following-back users
    not_following_back = [user for user in following if user not in followers]

    # Get profile URLs for not-following-back users
    not_following_back_urls = [following[user] for user in not_following_back]

    # Return the lists
    return not_following_back, not_following_back_urls

# Example usage (if you want to test the function within this file)
if __name__ == "__main__":
    not_following_back, not_following_back_urls = htmlExt()
    print("Users not following back:", not_following_back)
    print("Profile URLs of users not following back:", not_following_back_urls)
