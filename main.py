#A program to receive and display UK train service information
#Schedule to email train times every morning (after classes too?)
#GUI to input station and visualise services. Enable or disable GUI with a switch

import os
import logging
import customtkinter
import ttkbootstrap as ttk

from nredarwin.webservice import DarwinLdbSession
from dotenv import load_dotenv
from datetime import datetime

class Config():
    def __init__(self, env_file: str=".env"):
        self.load_config(env_file)

        self.arrival_switch = 2 #1 for arrival time, #2 for departure time
        self.max_services = 2 #Maximum number of services to display
        self.platform = 1 #Which platform to check
        self.crs = "MAN" #Remove hardcoding of station later

        #get apikey
        self.api_key = os.getenv("api_key")
        if self.api_key is None:
            logging.critical("API Key is empty")
            raise ValueError("API key is empty")
        
            
        

    def load_config(self, env_file: str=".env"):
        load_dotenv(env_file)


        
class TrainFetcher():

    def __init__(self, config: Config):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")
        
        self.root = customtkinter.CTk()

        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(True, True)
        self.root.geometry("500x500")
        self.root.title("Train track")
        #self.root.iconphoto(None)

        self.config = config
    
    def init_main_loop(self):
        self.root.mainloop()


    def service_disruption_check(self):
        pass

    def get_service_data(self):

        try:

            Darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=self.config.api_key)

            board = Darwin.get_station_board(crs=self.config.crs)
        
        except Exception as e:
            logging.critical(f"An error occured whilst trying to receive data via API: {e}")

        for service in board.train_services:
            if self.config.max_services <=0: #break loop after configured limit of services to be displayed is reached
                break
            
            destination = service.destination_text
            print (f"Destination : {destination}")
            if self.config.arrival_switch == 2:
                departure_time = service.std
                print (f"Departure time : {departure_time}")
            elif self.config.arrival_switch == 1:
                arrival_time = service.sta
                print (f"Arrival time: {arrival_time}")
            operator = service.operator_name
            print (f"TOC : {operator}")
            platform = service.platform
            print (f"Platform : {platform}")
            print ("------------------------------------------")

            self.config.max_services -= 1

if __name__ == '__main__':
    config = Config()
    program = TrainFetcher(config)
    program.init_main_loop()