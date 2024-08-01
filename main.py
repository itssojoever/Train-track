#A program to receive and display UK train service information
#Schedule to email train times every morning (after classes too?)

import os

from nredarwin.webservice import DarwinLdbSession
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

arrivalSwitch = 2 #1 for arrival time, #2 for departure time
maxServices = 2 #Maximum number of services to display
platform = 1 #Which platform to check

apiKey = os.getenv("apiKey")
CRS = os.getenv("CRS").upper().strip()

class trainFetcher():

    def serviceDisruptionCheck():
        pass

    def getServiceData(arrivalSwitch, maxServices):

        Darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=apiKey)

        board = Darwin.get_station_board(crs=CRS)

        services = Darwin.get_station_board(crs=CRS)

        for service in board.train_services:
            if maxServices <=0:
                break
            
            destination = service.destination_text
            print (f"Destination : {destination}")
            if arrivalSwitch == 2:
                departureTime = service.std
                print (f"Departure time : {departureTime}")
            elif arrivalSwitch == 1:
                arrivalTime = service.sta
                print (f"Arrival time: {arrivalTime}")
            operator = service.operator_name
            print (f"TOC : {operator}")
            platform = service.platform
            print (f"Platform : {platform}")
            print ("------------------------------------------")

            maxServices -= 1

trainFetcher.getServiceData(arrivalSwitch, maxServices)