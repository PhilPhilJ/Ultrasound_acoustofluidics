# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:44:40 2023

@author: s102772
"""

def switchvalve():
    import MXII_valve
    
    port_name = "COM4"
    #if the port has been cahnges it valve does not connect uncomment next line
    #port_name = None
    
    #find and connect to alve
    valve_address = MXII_valve.find_address(port_name)[0]
    valve = MXII_valve.MX_valve(valve_address, ports=10, name='My_valve', verbose=True)
    
    #switch valve position
    port = valve.get_port()
    if port == 1:
        valve.change_port(2)
    else:
        valve.change_port(1)
    
    del valve
    
    return

def CheckOpen():
    import MXII_valve
    
    port_name = "COM4"
    #if the port has been cahnges it valve does not connect uncomment next line
    #port_name = None
    
    #find and connect to alve
    valve_address = MXII_valve.find_address(port_name)[0]
    valve = MXII_valve.MX_valve(valve_address, ports=10, name='My_valve', verbose=True)
    
    #switch valve position
    port = valve.get_port()
    if port == 1:
        openport = True
    else:
        openport = False
    del valve
    
    return openport
    