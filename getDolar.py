import requests
from lxml import html
requisicao = requests.get ("https://www.dolarhoje.net.br/dolar-turismo/")
tree = html.fromstring(requisicao.content)
real = str(tree.xpath('//*[@id="mainContent"]/div/div[2]/div/div[4]/table[1]/tbody/tr[2]/td[1]/text()'))
dolar = str(tree.xpath('//*[@id="mainContent"]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/text()'))


print(str(real) + ' | '+ (dolar))