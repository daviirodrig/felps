import json
import os
from typing import Union

import twitch
from dotenv import load_dotenv

load_dotenv()
helix = twitch.Helix(os.environ["twitch_id"], os.environ["twitch_secret"])


def main(vod_id: Union[int, str]):
    count = 0
    for comment in helix.video(vod_id).comments:
        count += 1
        print(f"Processed {count} messages in {vod_id}", end="\r")

        if len(comment.message.emoticons) < 0:
            continue

        for emoticon in comment.message.emoticons:
            emote_name = comment.message.body[emoticon.begin : emoticon.end + 1]

            if not emote_name.startswith("felps"):
                continue

            emote = {
                "id": emoticon.id,
                "name": emote_name,
                "url": f"https://static-cdn.jtvnw.net/emoticons/v2/{emoticon.id}/default/dark/3.0",
                "color": "rosa",
                "is_variant": emoticon.id[-3] == "_",
                "is_community": False,
            }

            with open("categorized_emotes.json", "r+") as f:
                emotes: list = json.load(f)
                processed_emotes = [x["id"] for x in emotes]
                if emote["id"] not in processed_emotes:
                    emotes.append(emote)
                    f.seek(0)
                    f.write(json.dumps(emotes, indent=2))
                    f.truncate()
                    print(emote)

    print(f"Processed {count} messages in {vod_id}")
    # set vod as processed
    with open("processed.json", "r+") as f:
        vods = json.load(f)
        vods.append(str(vod_id))
        f.seek(0)
        f.write(json.dumps(vods, indent=2))
        f.truncate()


# main(1293985699)
