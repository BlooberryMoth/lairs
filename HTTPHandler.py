import ProfileHandler
from Main import Server


def handle_GET_request(url: list[str], parameters: dict) -> list[int, list[tuple[str, str]], str]:
    name, file_format, *_ = url[-1].split('.') + [""]
    if not file_format:
        if len(url):
            match url[0]:
                case "profile":
                    if len(url) == 1:
                        try: parameters["access_token"]
                        except: return 302, [("Location", "../")], ""
                    else: return ProfileHandler.fetch(name)
        try:
            with open(f'./http/{"/".join(url)}/index.html') as file_in: index = file_in.read()
            return 200, [("Content-Type", "text/html")], index
        except: return Server.fourohfour
    else:
        try:
            with open(f'./http/{"/".join(url)}') as file_in: file = file_in.read()
            return 200, [], file
        except: return Server.fourohfour