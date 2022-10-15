import json
import os
from typing import Dict, Iterable, List, Union

import twitch
from dotenv import load_dotenv

from msg_sender import send

load_dotenv()
helix = twitch.Helix(os.environ["twitch_id"], os.environ["twitch_secret"])

def read(filename) -> Union[Dict, List]:
    with open(filename, "r", encoding="utf-8") as f:
        j = json.load(f)
    return j


processed: List = read("processed.json")

def last_vods() -> Iterable:
    return helix.user("felps").videos(type='archive', first=100)


def main():
    vods = last_vods()
    not_processed = [x.id for x in vods if x.id not in processed]
    print(not_processed)
    for vod in not_processed:
        send(vod, 'vods_to_be_processed')

main()
