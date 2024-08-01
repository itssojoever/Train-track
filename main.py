#A program to receive and display UK train service information

import os

from nredarwin.webservice import DarwinLdbSession
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

maxServices = 2 #Maximum number of services to display
apiKey = os.getenv("apiKey")
CRS = os.getenv("CRS").upper().strip()

def getServiceData():

    Darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=apiKey)

    board = Darwin.get_station_board(crs=CRS)

    for service in board.train_services:
        if maxServices <=0:
            break
        
        destination = service.destination_text
        print (f"Destination : {destination}")
        dueStatus = service.etd
        print (f"Departure time : {dueStatus}")
        operator = service.operator_name
        print (f"TOC : {operator}")
        platform = service.platform
        print (f"Platform : {platform}")
        print ("------------------------------------------")

        maxServices -= 1