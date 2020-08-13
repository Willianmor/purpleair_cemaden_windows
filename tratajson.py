#import bibliotecas
import json
import requests
import ast
import uuid
from sqlalchemy import table, column
from sqlalchemy import create_engine,insert 
import time
from threading import Thread
from time import sleep

#import scripts auxiliares
from log import log
from log import logerro
from alert import alert
import temporizador
from temporizador import IntervalRunner
from alert import alert


#Função para tratar json
def trataJson(*args):
    try:
        #Estações principais

        #Números da estações: 25541|25891|31105|31101|31109|25503|31515|25499|31107|32451|25549|3968|25891|25541|31095|25525|31111|27843|25551|31091|31099|31115|25531|31089|13609|12364|39077

        #13609 não tem temperatura
        
        #define url 
        url = 'https://www.purpleair.com/json?key=IQWSYIVV2FJCFHX6&show=25541|25891|31105|31101|31109|25503|31515|25499|31107|32451|25549|3968|25891|25541|31095|25525|31111|27843|25551|31091|31099|31115|25531|31089|12364|39077|13609'
        #Requisitando link
        r = requests.get(url)
        #Criando um arquivo json
        files = r.json()
        
        #Criando arquivo final com apenas os resultados
        datafinal = files.get("results")
        
        print(datafinal[0]["ID"])

        print( str(datafinal[0]["ID"])+str(datafinal[0]["LastSeen"]))
        
        print ("_____________")
        print ("_____________")

        log()        
        for i in range (0,len(datafinal),2):
            #Conecção com o banco
            engine = create_engine('postgresql://postgres:123@localhost:5432/cemaden_pa')
            conn = engine.connect()
            #Inserção no banco
            result = conn.execute("INSERT INTO cemaden (idsensor,chave,Label,lat,lon, PM2_5Value,temp_f,humidity,pressure,p_0_3_um,p_0_5_um,p_1_0_um,p_2_5_um,p_5_0_um,p_10_0_um,pm1_0_cf_1,pm2_5_cf_1,pm10_0_cf_1,pm1_0_atm,pm2_5_atm,pm10_0_atm,LastSeen,LastUpdateCheck,Type) VALUES ({},'{}','{}',{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},'{}')".format(datafinal[i]["ID"],str(uuid.uuid4()),datafinal[i]["Label"],datafinal[i]["Lat"],datafinal[i]["Lon"], datafinal[i]["PM2_5Value"], datafinal[i].get("temp_f","NULL"), datafinal[i].get("humidity","NULL"), datafinal[i].get("pressure","NULL"),datafinal[i]["p_0_3_um"],datafinal[i]["p_0_5_um"],datafinal[i]["p_1_0_um"],datafinal[i]["p_2_5_um"],datafinal[i]["p_5_0_um"],datafinal[i]["p_10_0_um"],datafinal[i]["pm1_0_cf_1"],datafinal[i]["pm2_5_cf_1"],datafinal[i]["pm10_0_cf_1"],datafinal[i]["pm1_0_atm"],datafinal[i]["pm2_5_atm"],datafinal[i]["pm10_0_atm"],datafinal[i]["LastSeen"],datafinal[i]["LastUpdateCheck"],datafinal[i]["Type"]))
            #Encerrando conecção
            conn.close()

        #Estações secundárias
        
        #Números da estações: 25542|25893|31106|31102|31110|25504|31516|25500|31108|32452|25550|3969|25893|25542|31096|25525|31112|27844|25552|31092|31100|31116|25532|31090|13610|12365|39078

        #define url - 1 sensor
        url1 = 'https://www.purpleair.com/json?key=09SJEDDKBLPK75M6&show=25542|25893|31106|31102|31110|25504|31516|25500|31108|32452|25550|3969|25893|25542|31096|25525|31112|27844|25552|31092|31100|31116|25532|31090|13610|12365|39078'
        #Requisitando link
        r1 = requests.get(url1)
        files1 = r1.json()

        #Criando arquivo final com apenas os resultados
        datafinal2 = files1.get("results")

        for i in range (0,len(datafinal2),1):
            #Conecção com o banco
            engine = create_engine('postgresql://postgres:123@localhost:5432/cemaden_pa')
            conn = engine.connect()
            #inserção no banco
            result = conn.execute("INSERT INTO cemaden (idsensor,chave,Label,lat,lon, PM2_5Value,p_0_3_um,p_0_5_um,p_1_0_um,p_2_5_um,p_5_0_um,p_10_0_um,pm1_0_cf_1,pm2_5_cf_1,pm10_0_cf_1,pm1_0_atm,pm2_5_atm,pm10_0_atm,LastSeen) VALUES ({},'{}','{}',{},{},{},'{}',{},{},{},{},{},{},{},{},{},{},{},{})".format(datafinal2[i]["ID"],str(uuid.uuid4()),datafinal2[i]["Label"],datafinal2[i]["Lat"],datafinal2[i]["Lon"], datafinal2[i]["PM2_5Value"],datafinal2[i]["p_0_3_um"],datafinal2[i]["p_0_5_um"],datafinal2[i]["p_1_0_um"],datafinal2[i]["p_2_5_um"],datafinal2[i]["p_5_0_um"],datafinal2[i]["p_10_0_um"],datafinal2[i]["pm1_0_cf_1"],datafinal2[i]["pm2_5_cf_1"],datafinal2[i]["pm10_0_cf_1"],datafinal2[i]["pm1_0_atm"],datafinal2[i]["pm2_5_atm"],datafinal2[i]["pm10_0_atm"],datafinal2[i]["LastSeen"]))
            #Encerrando conecção
            conn.close()

    except Exception as e:
        print(e)
        logerro()
        alert()    
  
interval_monitor = IntervalRunner(60.0,trataJson)
interval_monitor.start()


#Reposta da função
resposta = input('Começou...\n')

