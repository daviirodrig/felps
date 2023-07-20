import json
import os
import time

import dotenv
import requests
from rich import print

dotenv.load_dotenv()
token_expiration = 0
token = ""


def fetch_emotes():
    client_id = os.environ["TWITCH_ID"]
    fetch_app_token()

    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {token}",
    }
    res = requests.get(
        "https://api.twitch.tv/helix/chat/emotes?broadcaster_id=30672329",
        headers=headers,
    )
    return res.json()


def fetch_app_token():
    global token_expiration
    global token
    if token_expiration > time.time():
        return token
    secret = os.environ["TWITCH_SECRET"]
    client_id = os.environ["TWITCH_ID"]
    res = requests.post(
        "https://id.twitch.tv/oauth2/token",
        data={
            "client_id": client_id,
            "client_secret": secret,
            "grant_type": "client_credentials",
        },
    )
    token_expiration = time.time() + res.json()["expires_in"]
    token = res.json()["access_token"]
    return res.json()


def get_stored_emotes():
    with open("categorized_emotes.json", "r") as f:
        return json.loads(f.read())


def check_emotes():
    current_emotes = get_stored_emotes()
    api_emotes = fetch_emotes()
    stored_ids = set()

    for emote in current_emotes:
        stored_ids.add(emote["id"])

    for emote in api_emotes["data"]:
        if emote["id"] not in stored_ids:
            print(
                f"New emote found: [green]{emote['id']}[/green] - [blue]{emote['name']}[/blue]"
            )
            # https://static-cdn.jtvnw.net/emoticons/v2/{{id}}/{{format}}/{{theme_mode}}/{{scale}}'
            print(
                f"https://static-cdn.jtvnw.net/emoticons/v2/{emote['id']}/default/dark/1.0"
            )

    pass


check_emotes()
