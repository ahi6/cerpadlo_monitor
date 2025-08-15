import requests
import configparser
import hashlib

def authenticate():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    config = cfg["DEFAULT"]

    address = config["ADDRESS"]
    url = f"http://{address}/LOGIN.XML"

    # get cookie
    response = requests.get(url)
    print("getting auth'd")

    if response.status_code != 200:
        raise Exception(f"[auth] HTTP code {response.status_code}")


    cookie_name = "SoftPLC"
    softplc_code = response.cookies[cookie_name]

    username = config["UNAME"]
    password = softplc_code + config["PASSW"]
    password = hashlib.sha1(password.encode('utf-8')).hexdigest() # cryptography

    # auth cookie
    headers = { 'Host': address, 'Content-Length': '54', 'Cache-Control': 'max-age=0', 'Origin': 'http://192.168.1.125', 'Content-Type': 'application/x-www-form-urlencoded', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://192.168.1.125/LOGIN.XML'}
    cookies = { 'SoftPLC': softplc_code, }
    data = { 'USER': username, 'PASS': password, }
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    print("got auth'd. yay!")

    # save cookie
    cfg["DEFAULT"]["COOKIE"] = softplc_code
    with open('config.ini', 'w') as configfile:
        cfg.write(configfile)

if __name__ == "__MAIN__":
    authenticate()
