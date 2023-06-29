import json

from jinja2 import Template


def build():
    with open("templates/template.html") as f:
        template = Template(f.read())

    with open("categorized_emotes.json", 'r') as f:
        emotes = json.load(f)
        emotes = sorted(emotes, key=lambda d: d['name'])

    obj = {
        "amarelo"  : [x for x in emotes if x["color"] == "amarelo" and x["is_variant"] is False],
        "laranja"  : [x for x in emotes if x["color"] == "laranja" and x["is_variant"] is False],
        "rosa"     : [x for x in emotes if x["color"] == "rosa" and x["is_variant"] is False],
        "community": [x for x in emotes if x["is_community"] is True],
        "variants" : [x for x in emotes if x["is_variant"] is True]
    }

    obj["outros"] = [x for x in emotes if x['id'] not in (*obj['amarelo'], *obj['laranja'], *obj['rosa'], *obj["community"])]

    rendered = template.render(emotes=obj)

    with open("index.html", "+w") as f:
        f.write(rendered)

build()
