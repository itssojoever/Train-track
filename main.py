#A program to receive and display UK train service information
#Schedule to email train times every morning (after classes too?)

import os
import logging
import customtkinter
import time


from nredarwin.webservice import DarwinLdbSession
from dotenv import load_dotenv
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Config():
    def __init__(self, env_file: str=".env"):
        self.load_config(env_file)

        self.color_theme = "dark-blue"
        self.appearance_mode = "system"

        self.arrival_switch = 2 #1 for arrival time, #2 for departure time
        self.max_services_options = ["1", "2", "3", "4", "5", "6", "7", "8"] #Maximum number of services to display
        self.max_services = 4
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
        
        customtkinter.set_appearance_mode(config.appearance_mode)
        customtkinter.set_default_color_theme(config.color_theme)
        
        self.root = customtkinter.CTk()

        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(True, True)
        self.root.geometry("500x495")
        self.root.title("Train Track")
        #self.root.iconphoto(None)

        self.config = config

        self.api_connection()
        self.create_gui()
        self.init_data_fetch()
        self.get_time()
        self.schedule_service_data()
    
    def init_main_loop(self):
        self.root.mainloop()

    def create_gui(self):

        self.frame_1 = customtkinter.CTkFrame(self.root)
        self.frame_1.pack(pady=20)

        self.label_1 = customtkinter.CTkLabel(self.frame_1, text="Select station:")
        self.label_1.grid(row=0, column=0, sticky="w")

        self.label_2 = customtkinter.CTkLabel(self.frame_1, text="Number of services to display:")
        self.label_2.grid(row=1, column=0, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.frame_1, values=self.config.crs, command=self.optionmenu_1_response)
        self.optionmenu_1.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.frame_1, values=self.config.max_services_options, command=self.optionmenu_2_response)
        self.optionmenu_2.set(value="4") #Set initial displayed value to 4
        self.optionmenu_2.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.service_display_1 = customtkinter.CTkTextbox(self.root, state="disabled", width=420, height=335)
        self.service_display_1.pack()

        self.time_label_1 = customtkinter.CTkLabel(self.root, font=("Helvetica", 24))
        self.time_label_1.pack()

    def api_connection(self, max_retries=3, wait_time=5):
        attempt = 0
        while attempt < max_retries:
            try:
                self.darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=self.config.api_key)
                return
        
            except Exception as e:
                attempt +=1
                logging.warning(f"Attempt {attempt} failed: {e}")
                if attempt < max_retries: 
                    time.sleep(wait_time)
                else:
                    logging.critical(f"An error occured whilst trying to receive data via API: {e}")
                    raise


    def optionmenu_1_response(self, crs_choice):
        self.station_chosen = crs_choice
        self.get_service_data(self.station_chosen)

    def optionmenu_2_response(self, max_services):
        self.config.max_services = int(max_services)
        self.get_service_data(self.station_chosen) #To update textbox instantly
        
    def init_data_fetch(self):
        initial_crs = self.config.crs[0]
        initial_max_services = 4
        self.optionmenu_1_response(initial_crs)
        self.optionmenu_2_response(initial_max_services)

    def get_time(self):
        time = datetime.now()
        self.formatted_time = time.strftime("%H:%M:%S")

        self.time_label_1.configure(text=f"Time:{self.formatted_time}")

        #Update once every 1000MS. I.E: a second
        self.root.after(1000, self.get_time)

    def service_disruption_check(self):
        pass #not implemented

    def crs_code_to_station_name(self, station_chosen): #Changes the CRS code to a full name string for the station
        return self.darwin.get_station_board(crs=self.station_chosen)

    def get_service_data(self, station_chosen):

        try:
            self.board = self.darwin.get_station_board(crs=station_chosen)
        
        except Exception:
            try:
                self.api_connection()
            except Exception as e:
                logging.critical(f"An error occured whilst trying to receive data via API: {e}")

        self.service_display_1.configure(state="normal")
        self.service_display_1.delete("1.0", "end")

        station_full_description = str(self.crs_code_to_station_name(station_chosen))
        station_full_description_slice = station_full_description[5:]

        chosen_station_output = (f"Displaying services for: {station_full_description_slice}\n"
                                 "===============================\n\n")
        
        self.service_display_1.insert("end", chosen_station_output)

        displayed_services = 0

        for service in self.board.train_services:
            if displayed_services >= self.config.max_services: #break loop after configured limit of services to be displayed is reached
                break
            
            destination = service.destination_text
            
            if self.config.arrival_switch == 1:
                arrival_time = service.sta
                
            elif self.config.arrival_switch == 2:
                departure_time = service.std
                
            operator = service.operator_name
            platform = service.platform

            service_output = (f"Destination: {destination}\n"
            f"Departure time: {departure_time}\n"
            f"Platform: {platform}\n"
            f"Provider: {operator}\n"
            f"------------------------------------------\n\n")

            self.service_display_1.insert("end", service_output)

            displayed_services += 1
        
        self.service_display_1.configure(state="disabled")

    def schedule_service_data(self):
        self.get_service_data(self.station_chosen)

        #Update once every 15000ms: four times a minute
        self.root.after(15000, self.schedule_service_data)

        logging.info(msg="New API call: services should update")

if __name__ == '__main__':
    config = Config()
    program = TrainFetcher(config)
    program.init_main_loop()