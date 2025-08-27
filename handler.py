def handle_GET_request(url: list[str], parameters: dict) -> list[int, list[tuple[str, str]], dict]:
    name, file_format, *_ = url[-1].split('.') + [""]
    if not file_format:
        try:
            with open(f'./http/{"/".join(url)}/index.html') as file_in: index = file_in.buffer.read()
            return 200, [("Content-Type", "text/html")], index
        except: return fourohfour
    else:
        try:
            with open(f'./http/{"/".join(url)}') as file_in: file = file_in.buffer.read()
            return 200, [], file
        except: return fourohfour

with open(f'./http/404/index.html') as file_in: index = file_in.buffer.read()
fourohfour = 404, [], index