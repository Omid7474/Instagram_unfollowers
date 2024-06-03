import json

def jsonExt(followers_file_path='followers_1.json', following_file_path='following.json'):
    # Read JSON files
    with open(followers_file_path) as followers_file:
        followers_data = json.load(followers_file)

    with open(following_file_path) as following_file:
        following_data = json.load(following_file)

    # Extract usernames from followers data
    followers = [entry['string_list_data'][0]['value'] for entry in followers_data]

    # Extract usernames from following data
    following = [entry['string_list_data'][0]['value'] for entry in following_data['relationships_following']]

    # Identify not-following-back users
    not_following_back = [user for user in following if user not in followers]

    # Get profile URLs for not-following-back users
    not_following_back_urls = [entry['string_list_data'][0]['href'] for entry in following_data['relationships_following'] if entry['string_list_data'][0]['value'] in not_following_back]

    # Return the lists
    return not_following_back, not_following_back_urls

# Example usage (if you want to test the function within this file)
if __name__ == "__main__":
    not_following_back, not_following_back_urls = jsonExt()
    print("Users not following back:", not_following_back)
    print("Profile URLs of users not following back:", not_following_back_urls)
