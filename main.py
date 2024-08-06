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
        self.max_services = 100 #Maximum number of services to display
        self.platform = 1 #Which platform to check
        self.crs = ["BHM", "BRV", "UNI"]

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

        self.create_gui()
        self.init_data_fetch()
    
    def init_main_loop(self):
        self.root.mainloop()

    def create_gui(self):
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.root, values=self.config.crs, command=self.optionmenu_1_response)
        self.optionmenu_1.pack(pady=20)

        self.service_display_1 = customtkinter.CTkTextbox(self.root, state="disabled", width=400)
        self.service_display_1.pack()

    def optionmenu_1_response(self, crs_choice):
        self.station_chosen = crs_choice
        self.get_service_data(self.station_chosen)
        
    def init_data_fetch(self):
        initial_crs = self.config.crs[0]
        self.optionmenu_1_response(initial_crs)



    def service_disruption_check(self):
        pass

    def get_service_data(self, station_chosen):

        try:

            Darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=self.config.api_key)

            board = Darwin.get_station_board(crs=station_chosen)

        
        except Exception as e:
            logging.critical(f"An error occured whilst trying to receive data via API: {e}")

        self.service_display_1.configure(state="normal")
        self.service_display_1.delete("1.0", "end")


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

            service_output = f"Destination: {destination}\n Departure time: {departure_time}\n\n"

            self.service_display_1.insert("end", service_output)

            self.config.max_services -= 1
        
        self.service_display_1.configure(state="disabled")

if __name__ == '__main__':
    config = Config()
    program = TrainFetcher(config)
    program.init_main_loop()