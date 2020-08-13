#-*- coding: utf-8 -*-

#Import bibliotecas
import json
import requests
import ast
import pandas as pd
from pandas.io.json import json_normalize
import uuid
from sqlalchemy import table, column
from sqlalchemy import create_engine,insert 
import time

#Import Scripts
import tratajson
from tratajson import trataJson 
import temporizador
from temporizador import IntervalRunner
from alert import alert
from log import log,logerro

def purpleair():
    tratajson()

resposta = input('Começou...\n')

