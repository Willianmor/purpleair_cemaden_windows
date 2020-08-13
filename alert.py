import win32api
import datetime

def alert():
    datainicio = str(datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S'))
    win32api.MessageBox(None,datainicio, 'ERRO NA COLETA') 
