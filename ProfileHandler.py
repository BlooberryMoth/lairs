from PIL import Image
import base64, json, os, bs4, HTTPHandler, io


def fetch(handle: str) -> str:
    with open(f'./http/profile/{handle}/info.json') as file_in: info = json.load(file_in)

    SOUP = bs4.BeautifulSoup(base_profile, features="html.parser")
    SOUP.title.string = f"{info['displayName']}'s Profile ({handle})"
    SOUP.find("img",  attrs={"avatar": ""})['src']    = f"/profile/{handle}/avatar.png"
    SOUP.find("img",  attrs={"banner": ""})['src']    = f"/profile/{handle}/banner.png"
    SOUP.find("p",    attrs={"bio": ""}).string       = info['bio']
    SOUP.find("span", attrs={"createdat": ""}).string = info['createdAt']
    SOUP.find("span", attrs={"deletedat": ""}).string = info['deletedAt']
    return 200, [], str(SOUP)
    

def update_avatar(handle: str, base64data: str):
    try: image_type, image_data = base64data.split(',')
    except: return HTTPHandler.error(400, "Invalid file/file type.")
    image_type = image_type.split('/')[1].split(';')[0]
    try:
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        img.save(f"./http/profile/{handle}/avatar.png")
    except: return HTTPHandler.error(400, "Bad file type.")
    return 200, [], ""


def update_banner(handle: str, base64data: str):
    try: image_type, image_data = base64data.split(',')
    except: return HTTPHandler.error(400, "Invalid file/file type.")
    image_type = image_type.split('/')[1].split(';')[0]
    try:
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        img.save(f"./http/profile/{handle}/banner.png")
    except: return HTTPHandler.error(400, "Bad file type.")
    return 200, [], ""


with open(f'./http/profile/base.html') as file_in: index = file_in.read()
base_profile = index