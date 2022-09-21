from bs4 import BeautifulSoup
from lxml import html
import requests
import pymongo
import datetime
import csv

conexao= pymongo.MongoClient("")
mydb= conexao['Cotacao']

date = datetime.date(2010,1,22)
today = datetime.date.today()
oneday = datetime.timedelta(days = 1)

date_counter = 0
def genDates(someDate):
    while someDate != today:
            someDate += oneday
            yield someDate
for d in genDates(date):
    date_counter += 1
    dia = int(d.day)
    mes = int(d.month)
    ano = int(d.year)
    if mes <10:
        smes = str(mes)
        cmes = "0" + smes
    else:
        cmes = str(mes)
    if dia <10:
        sdia = str(dia)
        cdia = "0" + sdia
    else:
        cdia = str (dia)

    textoano = str("https://www.noticiasagricolas.com.br/cotacoes/frutas/limao-tahiti-ceasas/%d" %ano)
    textomes = str(textoano + "-%s" %cmes)
    link = str(textomes + "-%s" %cdia)
    url = requests.get(link)
    soup=BeautifulSoup(url.content,'html.parser')

    data = soup.select('div.info div.fechamento')
    tipo = soup.select('div.table-content tbody tr') 

    for i in data:
        titulo= i.text
        titulo = titulo.split()

        for x in tipo:
            dados= x.text
            dadocerto = str(dados).split()

            databr = str("{}/{}/{}".format(cdia,cmes,ano))                         
            dataAtual = str(databr).split('/')[::-1]                         
            dataAtual = str(dataAtual[0] + '-' + dataAtual[1] + '-' + dataAtual[2])                         
            dataAtual = datetime.datetime.strptime(dataAtual, "%Y-%m-%d")

            if(dadocerto[0]=="Ceasa" or dadocerto[0]=="Ceagesp/SP" or dadocerto[0]=="Ceasa/Belo" or dadocerto[0]=="Ceasa/Campinas-SP" or dadocerto[0]=="Ceagesp/SP-SP"):
                pass
            else:
                if("/" in dadocerto[1]):
                    a = dadocerto[1].split("/")
                    dadocerto[1] = a[0]

                if("Sc/20" in dadocerto[1]):
                    dadocerto[1]="0.0"
                    dadocerto[2]="0.0"
                if("Sc/20" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if(dadocerto[1]=="S"):
                    dadocerto[1]="0.0"
                if(dadocerto[1]=="s"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="S"):
                    dadocerto[2]="0.0"
                if(dadocerto[2]=="s"):
                    dadocerto[2]="0.0"

                if(dadocerto[1]=="S/ cotação"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="S/ cotação"):
                    dadocerto[2]="0.0"

                if(dadocerto[1]=="s/cotação"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="s/cotação"):
                    dadocerto[2]="0.0"
                if(dadocerto[1]=="s/ cotação"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="s/ cotação"):
                    dadocerto[2]="0.0"
                if(dadocerto[1]=="Kg"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="Kg"):
                    dadocerto[2]="0.0"
                if(dadocerto[1]=="cotação/20"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="cotação/20"):
                    dadocerto[2]="0.0"
                if ("cotação" in dadocerto[1]):
                    dadocerto[2]="0.0"
                if ("cotação" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if ("cotação/" in dadocerto[1]):
                    dadocerto[2]="0.0"
                if ("cotação/" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if ("/Kg" in dadocerto[1]):
                    dadocerto[2]="0.0"
                if ("/Kg" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if ("/saca" in dadocerto[1]):
                    dadocerto[2]="0.0"
                if ("/saca" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if ("/kg" in dadocerto[1]):
                    dadocerto[2]="0.0"
                if ("/kg" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if ("/" in dadocerto[1]):
                    dadocerto[1]="0.0"
                if ("/" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if ("Sc/20" in dadocerto[2]):
                    dadocerto[2]="0.0"
                if ("Sc/20" in dadocerto[2]):
                    dadocerto[2]="0.0"
                

                if(dadocerto[1]=="***"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="***"):
                    dadocerto[2]="0.0"

                if(dadocerto[1]=="-"):
                    dadocerto[1]="0.0"
                if(dadocerto[2]=="-"):
                    dadocerto[2]="0.0"

                if(dadocerto[1]=="A"):
                    dadocerto[0]="Extra A"
                    if("," in dadocerto[2]):
                        dadocerto[1]=dadocerto[2]
                        if("," in dadocerto[3]):
                            dadocerto[2]=dadocerto[3]
                        else:
                            dadocerto[2]="0.0"
                    else:
                        dadocerto[1]="0.0"
                        if("-" in dadocerto[4]):
                            dadocerto[2]="0.0"
                        else:
                            ("," in dadocerto[3])
                            dadocerto[2]=dadocerto[3]
                
                if(dadocerto[1]=="B"):
                    dadocerto[0]="Especial B"
                    if("," in dadocerto[2]):
                        dadocerto[1]=dadocerto[2]
                        if("," in dadocerto[3]):
                            dadocerto[2]=dadocerto[3]
                        else:
                            dadocerto[2]="0.0"
                    else:
                        dadocerto[1]="0.0"
                        if("-" in dadocerto[4]):
                            dadocerto[2]="0.0"
                        else:
                            ("," in dadocerto[3])
                            dadocerto[2]=dadocerto[3]

                if(dadocerto[1]=="C"):
                    dadocerto[0]="Primeira C"
                    if(","in dadocerto[2]):
                        dadocerto[1]=dadocerto[2]
                        if("," in dadocerto[3]):
                            dadocerto[2]=dadocerto[3]
                        else:
                            dadocerto[2]="0.0"
                    else:
                        dadocerto[1]="0.0"
                        if("-" in dadocerto[4]):
                            dadocerto[2]="0.0"
                        else:
                            ("," in dadocerto[3])
                
                            dadocerto[2]=dadocerto[3]
                
                

                if("," in dadocerto[1]):
                    dadocerto[1] =dadocerto[1].replace(",", ".")
                if("," in dadocerto[2]):
                    dadocerto[2] =dadocerto[2].replace(",", ".")
                


                preco= float(dadocerto[1])
                variacao = float(dadocerto[2])

                with open("dado.csv", 'a', newline='') as saida:
                        escrever = csv.writer(saida)
                        escrever.writerow((dataAtual, dadocerto[0], preco, variacao))


                print ('DATA : {} || DADOS : {}'.format(titulo[1],dadocerto))
                mydb.Limao.update(
                    {
                        "data":dataAtual,
                        "tipo":dadocerto[0],
                        "preco":preco,
                        "variacao":variacao
                    },
                    {
                        "data":dataAtual,
                        "tipo":dadocerto[0],
                        "preco":preco,
                        "variacao":variacao 
                    },
                    upsert = True


                )
