from lxml import html
import requests
import json

def getJob():
    requisicao = requests.get ("https://www.geekhunter.com.br/vagas?acceptRemote=true&salaryType%5B%5D=clt")
    tree = html.fromstring(requisicao.content)
    date = str(tree.xpath('//*[@id="page-content"]/div[1]/div[1]/div[2]/p/b[1]/text()'))

    #Tratamento dos dados
    date = date.split()
    dateReplace = date[0].replace('[', '')
    numberJob = dateReplace.replace("'", '')

    print("Total de vagas CLT: ", numberJob)

getJob()