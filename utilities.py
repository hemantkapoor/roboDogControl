import os
import psutil
import time

def get_cpu_tempfunc():
    """ Return CPU temperature """
    result = 0
    mypath = "/sys/class/thermal/thermal_zone0/temp"
    with open(mypath, 'r') as mytmpfile:
        for line in mytmpfile:
            result = line

    result = float(result)/1000
    result = round(result, 1)
    return result

def get_cpu_use():
    """ Return CPU usage using psutil"""
    cpu_cent = psutil.cpu_percent()
    return cpu_cent


def get_ram_info():
    """ Return RAM usage using psutil """
    ram_cent = psutil.virtual_memory()[2]
    return ram_cent

if __name__ == '__main__':
    print("Test utilities")
    temp = get_cpu_tempfunc()
    print("Temperature = " + str(temp))

    print("Cpu Stats = " + str(get_cpu_use()))
    print("Cpu Ram Info = " + str(get_ram_info()))

