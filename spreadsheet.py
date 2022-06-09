from __future__ import print_function  
from googleapiclient.discovery import build  
from httplib2 import Http  
from oauth2client import file, client, tools  
from oauth2client.service_account import ServiceAccountCredentials  
from threading import Timer

MY_SPREADSHEET_ID = '1y-J0WfXE7Yc1T4_gV8P7SmNAb-qUffZR0y-cIGodcRc'

jsonValues = []

def Hel():
	print("yey")


while True:
	t = Timer(30.0, Hel)
	t.start()
	
