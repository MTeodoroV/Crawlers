import time
import pymongo
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# teste = os.environ.get("MONGO_ROOT")
# teste2 = os.environ.get("CONEXAO_MONGO")



def startConection():
# conexao = pymongo.MongoClient("")
    conexao = pymongo.MongoClient(os.environ.get("${teste}"))
    mydb = conexao['Jobs']
    return mydb
# mydb = conexao[os.environ.get("${teste2}")]

startConection()

vaga = {'Vagas' : '350'}
insere = mydb.vagas.insert_one(vaga)


# SECRET_KEY = os.environ.get("MONGO_ROOT")
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")