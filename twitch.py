import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Twitch credentials from the .env file
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")


def get_access_token(client_id, client_secret):
    """
    Obtain an access token from Twitch using the Client Credentials Flow.
    """
    # Twitch endpoint for obtaining the access token
    url = "https://id.twitch.tv/oauth2/token"
    
    # Parameters for the access token request
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    
    # Make a POST request to get the token
    response = requests.post(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        access_token = json_response.get("access_token")
        print("Access Token:", access_token)
        return access_token
    else:
        print("Failed to obtain access token.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None

def get_user_id(access_token, user_login):
    """
    Get the user ID for a given Twitch username (user_login).
    """
    url = "https://api.twitch.tv/helix/users"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    params = {"login": user_login}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        json_response = response.json()
        users = json_response.get("data", [])
        if users:
            return users[0].get("id")
    print("Failed to obtain user ID.")
    return None

def get_streamer_highlights(access_token, user_login):
    """
    Fetch and print highlights of a specific streamer, ordered by date.
    """
    user_id = get_user_id(access_token, user_login)
    if not user_id:
        return

    url = "https://api.twitch.tv/helix/videos"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "user_id": user_id,
        "type": "highlight",
        "sort": "trending",  # This ensures the results are ordered by date
        "period": "week"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        json_response = response.json()
        highlights = json_response.get("data", [])
        for highlight in highlights:
            print(f"Title: {highlight['title']}, URL: {highlight['url']}, Date: {highlight['created_at']}")
    else:
        print("Failed to obtain streamer highlights.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
