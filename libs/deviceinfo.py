import sys
import subprocess

SUPPORTED_DEVICES = [
    {
        "name" : "Linux PC",
        "serial_number_command" : "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
    },
    {
        "name" : "Windows PC",
        "serial_number_command" : "wmic bios get serialnumber"
    },
    {
        "name" : "Raspberry Pi",
        "serial_number_command" : "cat /sys/firmware/devicetree/base/serial-number"
    },
    {
        "name" : "Jetson Nano",
        "serial_number_command" : "cat /sys/firmware/devicetree/base/serial-number"
    },
]

class __Device:
    """
    Device Object
    """

    #config
    __device_type = 0
    __device_id = ""

    def __init__(self):
        """
        Get used device info
        """
        os_type = sys.platform.lower()
        if "win" in os_type:
            self.__device_type = 1
        elif "linux" in os_type:
            device_name = str(subprocess.check_output("cat /proc/device-tree/model", shell=True).decode("utf-8")).replace("\n","").replace("\r","").replace("\x00","").replace("SerialNumber","")
            self.__device_type = next(iter([ i for i, device in enumerate(SUPPORTED_DEVICES) if device["name"] in device_name]), 0)

        self.__device_id = subprocess.check_output(SUPPORTED_DEVICES[self.__device_type]["serial_number_command"], shell=True).decode("utf-8").replace("\n","").replace("\r","").replace("\x00","").replace(" ","").replace("SerialNumber","")
    
    def gettype(self):
        return self.__device_type
    
    def getname(self):
        return SUPPORTED_DEVICES[self.__device_type]["name"]
    
    def getid(self):
        return self.__device_id

device = __Device()

def main():
    print("Device type: ",device.gettype())
    print("Device name: ",device.getname())
    print("Device id: ",device.getid())

if __name__ == '__main__':
    main()