from bs4 import BeautifulSoup
from lxml import html
import requests
import pymongo
import datetime

conexao = pymongo.MongoClient("")
mydb = conexao["Cotacao"]

request= requests.get("https://www.noticiasagricolas.com.br/cotacoes/laranja/laranja-ceasas")

soup= BeautifulSoup(request.content,'html.parser')
data = soup.select("div.fechamento") 
tabela = soup.select("div.table-content table.cot-fisicas tbody tr")

date= datetime.date(2010,1,4)
today= datetime.date.today()
oneday= datetime.timedelta(days = 1)

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
        if mes < 10:
                  smes= str(mes)
                  cmes= "0"+smes
        else:
                  cmes=str(mes)
        if dia < 10:
                  sdia = str(dia)
                  cdia = "0"+sdia
        else:
                  cdia=str(dia)
        
        textoano = str("https://www.noticiasagricolas.com.br/cotacoes/laranja/laranja-ceasas/%d" %ano)
        textomes = str(textoano+"-%s" %cmes)
        link = str(textomes+"-%s" %cdia)
        url = requests.get(link)
        soup = BeautifulSoup(url.content,"html.parser")
        tipo = soup.select("div.table-content tbody tr")
        data = soup.select("div.info div.fechamento")

                  
        for i in data:
            item = i.text
            item = item.split()

            for y in tabela:
                item3 = y.text
                dados = str(item3).split()
                
                databr = str("{}/{}/{}".format(cdia,cmes,ano))                         
                dataAtual = str(databr).split('/')[::-1]                         
                dataAtual = str(dataAtual[0] + '-' + dataAtual[1] + '-' + dataAtual[2])                         
                dataAtual = datetime.datetime.strptime(dataAtual, "%Y-%m-%d")
            
                if (dados[0]== "Laranja"):
                    dados[0]= "{} {} {}".format(dados[0],dados[1],dados[2])         
                    if(dados[2].startswith("B")):
                        if(dados[3]=="S/"):
                            dados[1]="0.0"
                        if(dados[4]=="-"):
                            dados[2]="0.0"
                        else:
                            dados[2]=dados[4]
                    if(dados[2].startswith("Grande")):
                        if(dados[3]=="S/"):
                            dados[1]="0.0"
                        if(dados[4]=="-"):
                            dados[2]="0.0"
                        else:
                            dados[2]=dados[4].replace("," , ".")         
                    if(dados[2].startswith("Extra")):
                        if(dados[3]=="S/"):
                            dados[1]="0.0"
                        if(dados[4]=="-"):
                            dados[2]="0.0"
                        else:
                            dados[1]=dados[3]
                            dados[2]=dados[4]
                    else:
                        dados[1]=dados[3]
                    if("," in dados[1]):
                        dados[1] =dados[1].replace(",", ".")
                    if("," in dados[2]):
                        dados[2] =dados[2].replace(",", ".")
                    if(dados[1]=="S/"):
                    
                        dados[1]="0.0"
                        dados[2]=dados[3]
                    if(dados[2]=="S/"):
                        dados[2]="0.0"

                    print((item[1],dados))
                        
                    data = dataAtual
                    tipo = dados[0]
                    preco= float(dados[1])
                    variacao= float(dados[2])

                    mydb.Laranja.update(
                                        {
                                                "data" : data,
                                                "tipo" : tipo,
                                                "preco": preco,
                                                "variacao": variacao
                                      
                                        },
                                        {
                                                "data" : data,
                                                "tipo" : tipo,
                                                "preco": preco,   
                                                "variacao": variacao
                                        },
                                            upsert=True                    
                                        )
                    
                    

                else:
                    pass
