import os
import yaml
import socket
import struct
import binascii

from datetime import datetime

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



# load config
with open("/config/config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Get local IP and start listening for WOL packets
ip = get_ip()
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((ip, config['wol_port']))


print("Listening for WOL on " + ip + "\n")


while True:

    data, (from_ip, from_port) = sock.recvfrom(1024) # buffer size is 1024 bytes

    # convert data to hex, get just the MAC, and convert to ascii
    hex_data  = binascii.hexlify(data,":")
    mac = hex_data[18:35].decode('ascii').upper()
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print("WOL Received from " + from_ip + " for MAC " + mac)

#    f = open("/logs/wol_log.txt", "a")
#    f.write(dt_string + ":\t from " + from_ip + "\t for " + mac + "\n")

    try:
        if mac in config['devices']:
            cmd = config['devices'][mac]['cmd']

            print("MAC Address found.  Executing cmd: " + cmd)

            os.system(cmd)
            print("Success")
#            f.write("  - cmd: " + cmd + "\n")
        else:
            print("MAC Address not in config")
#            f.write("  - MAC Address not in config\n")

    except:
            print("Failed")

#        f.write("An exception occurred\n")
#        f.close()