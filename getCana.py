from bs4 import BeautifulSoup
from lxml import html
import requests
import datetime
import pymongo

conexao = pymongo.MongoClient("")
mydb = conexao['Cotacao']


date = datetime.date(2018,1,1)
today = datetime.date.today()
oneday= datetime.timedelta(days =1)

date_counter = 0
def genDates(someDate):
    while someDate != today:
        someDate += oneday
        yield someDate
for d in genDates(date):
    date_counter +=1
    dia = int (d.day)
    mes = int (d.month)
    ano = int (d.year)
    if mes <10:
        smes = str(mes)
        cmes = '0'+ smes
    else:
        cmes = str(mes)
    if dia <10:
        sdia = str (dia)
        cdia = '0' + sdia
    else:
        cdia = str(dia)
        
    textoano = str ('https://www.noticiasagricolas.com.br/cotacoes/sucroenergetico/acucar-preco-da-cana-basica-pr/%d' %ano)
    textomes = str (textoano +'-%s' %cmes)
    link = str (textomes + '-%s' %cdia)
    url = requests.get(link)
    soup = BeautifulSoup(url.content, 'html.parser')
    tipo = soup.select('div.table-content table.cot-fisicas tbody tr')
    data = soup.select('div.fechamento')

    for i in data:
        data = i.text
        data = data.split()
        for y in tipo:
            dado = y.text
            dado = str(dado).split()

            databr = str("{}/{}/{}".format(cdia,cmes,ano))                         
            dataAtual = str(databr).split('/')[::-1]                         
            dataAtual = str(dataAtual[0] + '-' + dataAtual[1] + '-' + dataAtual[2])                         
            dataAtual = datetime.datetime.strptime(dataAtual, "%Y-%m-%d")

            if((dado[0]=="Campo") or (dado[0]== "Esteira")): 
                if("," in dado[1]):
                    dado[1] = dado[1].replace("," , ".")
                if("+" in dado[2]):
                    dado[2] = dado[2].replace("+" , "")
                if("-" in dado[2]):
                    dado[2] = dado[2].replace("-" , "")    
                if("," in dado[2]):
                    dado[2] = dado[2].replace("," , ".")    
                
                dado[1] = float(dado[1])
                dado[2] = float(dado[2]) 

                mydb.Cana.update(
                    {
                        "data" : dataAtual,
                        "tipo" : dado[0],
                        "preco" : dado[1],
                        "variacao" : dado[2]
                    },
                    {
                        "data" : dataAtual,
                        "tipo" : dado[0],
                        "preco" : dado[1],
                        "variacao" : dado[2]

                    },
                    upsert = True

                )
                    


                print('DATA : {} || DADOS : {}'.format(data[1],dado))
            else:
                pass

