import json, os, bs4
from Main import Server


def fetch(account: str):
    if not os.path.exists(f'./http/profile/@{account.removeprefix("@")}'): return Server.fourohfour
    else:
        if not account.startswith('@'): return 308, [("Location", f"./@{account}")], ""

        with open(f'./http/profile/{account}/info.json') as file_in: info = json.load(file_in)

        SOUP = bs4.BeautifulSoup(base_profile, features="html.parser")
        SOUP.title.string = f"{info['displayName']}'s Profile (@{account.removeprefix('@')})"
        SOUP.find("img", attrs={"avatar": ""})['src'] = f"/profile/{account}/avatar.png"
        return 200, [], str(SOUP)

with open(f'./http/profile/base.html') as file_in: index = file_in.read()
base_profile = index