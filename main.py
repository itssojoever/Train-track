#A program to receive and display UK train service information
#Schedule to email train times every morning (after classes too?)
#GUI to input station and visualise services. Enable or disable GUI with a switch

import os
import ttkbootstrap as ttk

from nredarwin.webservice import DarwinLdbSession
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

arrival_switch = 2 #1 for arrival time, #2 for departure time
max_services = 2 #Maximum number of services to display
platform = 1 #Which platform to check

apiKey = os.getenv("apiKey")
CRS = os.getenv("CRS").upper().strip()

class trainFetcher():

    def __init__(self):
        self.root = ttk.Window(themename="superhero")
        self.root.position_center()
        self.root.resizable(True, True)
        self.root.geometry("500x500")
        self.root.title("Train track")
        self.root.iconname(None)
    
    def initMainLoop(self):
        self.root.mainloop()


    def service_disruption_check():
        pass

    def get_service_data(arrival_switch, max_services):

        Darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=apiKey)

        board = Darwin.get_station_board(crs=CRS)

        for service in board.train_services:
            if max_services <=0:
                break
            
            destination = service.destination_text
            print (f"Destination : {destination}")
            if arrival_switch == 2:
                departure_time = service.std
                print (f"Departure time : {departure_time}")
            elif arrival_switch == 1:
                arrival_time = service.sta
                print (f"Arrival time: {arrival_time}")
            operator = service.operator_name
            print (f"TOC : {operator}")
            platform = service.platform
            print (f"Platform : {platform}")
            print ("------------------------------------------")

            maxServices -= 1

if __name__ == '__main__':
    program = trainFetcher()
    program.initMainLoop()