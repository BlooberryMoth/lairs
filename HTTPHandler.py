import base64, json, ProfileHandler
from Main import Server


def handle_GET_request(url: list[str], parameters: dict) -> tuple[int, list[tuple[str, str]], str]:
    name, file_format, *_ = url[-1].split('.') + [""]
    if not file_format:
        if len(url):
            match url[0]:
                case "profile":
                    if len(url) == 1:
                        try: parameters["access_token"]
                        except: return 302, [("Location", "../")], ""
                    elif len(url) == 2: return ProfileHandler.fetch(name)
        try:
            with open(f'./http/{"/".join(url)}/index.html') as file_in: index = file_in.buffer.read()
            return 200, [("Content-Type", "text/html")], index
        except: return Server.fourohfour
    else:
        try:
            with open(f'./http/{"/".join(url)}') as file_in: file = file_in.buffer.read()
            return 200, [], file
        except: return Server.fourohfour


def handle_POST_request(data: bytes) -> tuple[int, list[tuple[str, str]], str]:
    try: data = json.loads(data.decode())
    except: return error(400, "Invalid body form.")
    try: method = data['method']
    except: return error(400, "No method provided.")

    match method:
        case "fileUP/image":
            try: location = data['location']
            except: return error(400, "No location provided for image upload.")
            if location not in ["avatar", "banner", "post"]: return error(400, "Invalid location for image upload")
            try: image_type, image_data = data['data'].split(',')
            except: return error(400, "Invalid file/file type.")
            image_type = image_type.split('/')[1].split(';')[0]

            if image_type == "png":
                with open('./http/profile/@lairs/avatar.png', 'wb') as file_out: file_out.write(base64.b64decode(image_data))
                return 200, [], ""

def error(status: int, reason: str): return status, [("Content-Type", "application/json")], json.dumps({"error": status, "reason": reason})