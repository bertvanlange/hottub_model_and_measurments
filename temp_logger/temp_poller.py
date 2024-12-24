import minimalmodbus

import serial
import serial.tools.list_ports
import time
import csv
import shutil
from datetime import datetime
import os

# get the name of the port for the serial connection

def find_ftdi_port():
    """Find the FTDI USB-to-Serial converter port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Check if the device description or manufacturer matches FTDI
        if "FTDI" in (port.manufacturer or "") or "FTDI" in (port.description or ""):
            return port.device
    return None


def open_tempeture_divice(com_port,id = 1, baud = 9600):
    instrument = minimalmodbus.Instrument(com_port, id)  # port name, slave address (in decimal)
    instrument.serial.port = com_port                     # this is the serial port name
    instrument.serial.baudrate = baud         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 1        # seconds
    instrument.address = 1                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU
    return instrument

# divice = open_tempeture_divice("COM4")

def read_temp(debug =  False):
    # find serial port
    com_port = find_ftdi_port()
    if(com_port == None):
        print("ERROR: FTDI divice not found")
        return None
    else:
        if debug :
            print(f"FTDI divice found on port {com_port}")
        

    # open modbus_divice
    try:
        divice = open_tempeture_divice(com_port)
    except Exception as e:
        print(f"Open modbus Error: {e}")
        return None
    
    # read registers
    try:
        # Read 10 registers starting from address 0
        registers = divice.read_registers(0, 4)  # 0 is the starting address, 10 is the number of registers to read
        if debug :
            print(f"raw registers{registers}")
        # print(f"Registers: {registers}")
        return [0 if num > 2000 else num / 10 for num in registers]
    except Exception as e:
        print(f"Reading modbus Error: {e}")
        return None





# Initialize the CSV file with headers if it doesn't exist
def initialize_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4"])
        print(f"Initialized {file_path}.")

# Log a single entry to the CSV file
def log_to_csv(file_path, timestamp, temperatures):
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp] + temperatures)
    print(f"Logged: {timestamp}, {temperatures}")

def create_backup(log_file):
    

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(backup_log, f"temperature_backup_{timestamp}.csv")
    try:
        shutil.copy(log_file, backup_file)
        print(f"Backup created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Failed to create backup: {e}")

if __name__ == "__main__":

    # settup for logging
    log_dir = os.path.join(os.path.dirname(__file__), "logs")  # Logs folder in the script's directory
    log_file = os.path.join(log_dir, "temperature_log.csv")  # Main log file
    backup_log = os.path.join(log_dir, "back_ups")  # Logs folder in the script's directory
    # Ensure the logs folder exists
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(backup_log, exist_ok=True)

    initialize_csv(log_file)
    start_time = time.time()  # For tracking 10-minute backup intervals

    while True:
        temp = read_temp()
        if(temp ==  None):
            print("temp is none, tempeture not read")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_to_csv(log_file, timestamp, temp)
            
            if time.time() - start_time >= 300:  # 30 seconds = 5 minutes
                create_backup(log_file)
                start_time = time.time()  # Reset the timer
        
        time.sleep(5)
