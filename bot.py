import requests
from lxml import html

requisicao = requests.get('https://www.mercadobitcoin.com.br/negociacoes') 

tree = html.fromstring(requisicao.content)

contador = 1 
linha = 1 

print(soup)

while linha <21: 
	quantidade = str(tree.xpath('//*[@id="orderbook-list"]/div[1]/table/tbody/tr[%d]/td[1]/text()' %contador))
	preco = str(tree.xpath('//*[@id="orderbook-list"]/div[1]/table/tbody/tr[%d]/td[2]/text()' %contador))
	quantidade = str(tree.xpath('//*[@id="orderbook-list"]/div[2]/table/tbody/tr[%d]/td[1]/text()' %contador))
	
	teste= str(tree.xpath('//*[@id="trading-panel"]/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div/div[1]/span[1]'))

	print (str(quantidade)+' | '+str(preco)+' | '+str(quantidade)) 
	linha = linha + 1 
	contador = contador + 1 

print(teste)
print ('FIM DO BOT') 