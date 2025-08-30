import json, os, ProfileHandler
from Main import Server


def handle_GET_request(url: list[str], parameters: dict) -> tuple[int, list[tuple[str, str]], str]:
    name, file_format, *_ = url[-1].split('.') + [""]
    if not file_format:
        if len(url):
            match url[0]:
                case "profile":
                    if len(url) == 1:
                        try: parameters['access_token']
                        except: return 302, [("Location", "/")], ""
                    elif len(url) == 2:
                        if url[1] == "edit":
                            try: parameters['access_token']
                            except: return 302, [("Location", "/login")], ""
                        else:
                            if not name.startswith('@'): return 308, [("Location", f"./@{name}")], ""
                            for account in os.listdir('./http/profile'):
                                if name in os.listdir(f'./http/profile/{account}'): break
                            else: print("test")
                            return ProfileHandler.fetch(account)
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
            match location:
                case "avatar": return ProfileHandler.update_avatar("@lairs", data['data'])
                case "banner": ...
                case "post": ...
                case _: return error(400, "Invalid location.")
        case "checkEmail":
            try: login = data['data'].lower()
            except: return error(400, "Invalid email provided.")
            if f"@{login.removeprefix('@')}.json" in os.listdir('./accounts'): return 200, [("Content-Type", "application/json")], json.dumps({"found": True})
            

def error(status: int, reason: str): return status, [("Content-Type", "application/json")], json.dumps({"error": status, "reason": reason})