from twitch import get_access_token, get_streamer_highlights
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Twitch credentials from the .env file
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

if __name__ == "__main__":
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if access_token:
        streamer_username = "smzinho"  # Replace with the streamer's username
        get_streamer_highlights(access_token, streamer_username)