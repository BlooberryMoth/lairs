import os, bs4
from Main import Server


def fetch(account: str):
    if not os.path.exists(f'./http/profile/@{account.removeprefix("@")}'): return Server.fourohfour
    else:
        SOUP = bs4.BeautifulSoup(base_profile, features="html.parser")
        SOUP.title.string = f"@{account.removeprefix('@')}'s Profile"
        return 200, [], str(SOUP)

with open(f'./http/profile/base.html') as file_in: index = file_in.read()
base_profile = index