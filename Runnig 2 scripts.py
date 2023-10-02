# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 14:55:21 2023

@author: s102772
"""
import multiprocessing
from pypylon import pylon
import serial, time
import cv2
import sys
sys.path.append('C:/Users/s102772/Desktop/Ultrasound_acoustofluidics/')
from AD_func import *
#from frameCut import *
import numpy as np
import numpy as np
from pypylon import pylon
import cv2
import sys
sys.path.append(r'C:\Users\s102772\Desktop\Ultrasound_acoustofluidics')
from ThorlabsFunctions import *
import time
from AD_func import *
from freqSweep import *

  
def Video(a):
    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    """
    Created on Mon Aug 21 10:55:36 2023

    @author: joakimpihl
    """

    # Code for generating the first recording op particle focusing to be used for practice of image analysis

    #from pypylon import pylon
    #import serial, time
    #import cv2
    #import sys
    #sys.path.append('C:/Users/s102772/Desktop/Ultrasound_acoustofluidics/')
    #from AD_func import *
    #from frameCut import *
    #import numpy as np

    print('Press ESC to close the window')

    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    #cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
    size = (4504, 4504) # Camera resoloution: 4504x4504px, FPS: 18
    FPS = 18 # Frames per second of camera
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Defines output format, mp4
    out = cv2.VideoWriter('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4', fourcc, FPS, size) #Change path to saved location

    #Connect to analog discovery
    Connect()
    #t = 1
    #test = 0
    record = -10
    start = time.time()
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
     #   test += 1
        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
    # =============================================================================
    #         if t==42:
    #             img = img[:,IL:IR]
    # =============================================================================
            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
            cv2.imshow('Algae experiment', img)
            k = cv2.waitKey(1)
            if k == ord('r'): # press down r to record
                record = True
                print('Starting recording..')
            elif k == ord('s'): #Stop recording
                record = False    
                print('Stopping recording..')
            if record:
                out.write(img)
            if k == ord('f'): # press f
                funcGen()
            if k == ord('p'): # press F
                funcGen(freq=3.82)
            if k == ord('g'): # press g
                funcStop()
                
    ################################### Deletes unwanted data
    # =============================================================================
    #         if t == 5:
    #             IL,IR = frameCut(img)
    #         if t<6:
    #             t+=1
    #         elif t!=42:
    #             t=42
    # =============================================================================
    ###########################################         
                         
    # Close experiment
            if k == 27: # press ESC
                cv2.destroyAllWindows()
                disconnect()
                break
    # =============================================================================
    #         stop = time.time()
    #         if (stop-start >= 10):
    #             print('Delta_T: ' + str(stop-start))
    #             print('expected loops = 10s * 18FPS = 180frames')
    #             print('Loops: ' + str(test))
    # =============================================================================
        grabResult.Release()

        
    # Releasing the resource   
    out.release() 
    camera.StopGrabbing()


  
def Thor(a):
    #import numpy as np
    #from pypylon import pylon
    #import cv2
    #import sys
    #sys.path.append(r'C:\Users\s102772\Desktop\Ultrasound_acoustofluidics')
    #from ThorlabsFunctions import *
    #import time
    #from AD_func import *
    #from freqSweep import *

    #%%
    ###############################################################################
    ### Move to position

    ## Set homed
    Homed = True

    if Homed == False:
        print("Homing...")

        HomeX()
        HomeAll()

    print("The device is homed in all directions")

    ### Input the starting position (bottom position of the tube) and top position. Make sure the device has not been moved since
    ### last use.

    coordinate_bottom =  [43.04160, 26.24083, 28.9598]
    coordinate_top =  [43.04160, 26.24083, 43.62598]

    tube_length = coordinate_top[2] - coordinate_bottom[2]
    print("coordinate_bottom is " + str(coordinate_bottom) + "and coordinate_top is " + str(coordinate_top) + " and the tube length is " + str(tube_length))

    #print("It is important that the GCTH has not been moved since last use because the camara could move in to the holder. The coodinate is set to: "+ str(coordinate_bottom))
    #user_input = input('Would you like to continue (y/n)')

    #if user_input.lower() == 'y':
        #print('user typed "y" and the program will continue')
    #elif user_input.lower() == 'n':
        #sys.exit('user typed "n" and the program will terminate now')
    #else:
        #print('Type "y" or "n"')

    print("moving to starting position")
    MoveRelY(coordinate_bottom[1])
    MoveRelZ(coordinate_bottom[2])
    MoveRelX(coordinate_bottom[0])

    print("The device is now in the starting position")

    #%%
    ###############################################################################
    ### Doing analysis of capillary tube

    ## Initialize camara


    #Connect to analog discovery
    Connect()

    #number of runs for characterization of tube. note that the tube length is given and one frame is 0.84 mm therefore the number 
    #should be tube_length/frame_height but could be more.
    move_length = 0.84
    runs = np.ceil(tube_length / move_length)
    run_count = runs

    #frequency for focusing
    frequency = 3.82 

    #voltages for the tone generator
    volts = [1, 10, 20]

    #start and stop frequencies for sweep
    sweep = [3, 5]

    #Connect to analog discovery
    Connect()

    #print("Characterization of tube is about to begin and will run for ")
    #user_input = input('Would you like to continue (y/n)')

    #if user_input.lower() == 'y':
        #print('user typed "y" and the program will continue')
    #elif user_input.lower() == 'n':
        #sys.exit('user typed "n" and the program will terminate now')
    #else:
        #print('Type "y" or "n"')
        

    #the current position of the camera
    position = coordinate_bottom

    #counter for while loop
    count = 0

    #wait times
    wait_time = 1

    #creating statements
    background = True
    first = True
    doing_volts = False
    doing_sweeps = False
    move = False

    position = [PositionX(), PositionY(), PositionZ()]

    while run_count > 0:
        #messuring the time
        current_time = time.time()
        
        ### Making background
        
        while background == True:
            
            new_time = time.time()
            
            if first == True:
                print("making a background image over " +str(wait_time) + " s")
                first = False
            
            if current_time + wait_time < new_time:
                
                print("making a background done")
                background = False
                doing_volts = True
                first = True
                current_time = time.time()
                
        ### focusing at different amplitudes
         
        
        while doing_volts == True:
        
            new_time = time.time()
            
            if first == True:
                print("Now focusing...")
                funcGen(freq=frequency, Amplitude=volts[count])
                first = False
            
            if current_time + wait_time < new_time:
                
                print("Focusing at freguency: " + str(frequency) + " Hz and amplitude: " + str(volts[count]) + " V")
                first = True
                doing_sweeps = True
                count += 1
                current_time = time.time()
                
                if count == len(volts):
                    
                    doing_volts = False
                    count = 0

        
        ### doing sweeps in frequencies
        
        
        #this part is not done yet and only does a print-statement
        while doing_sweeps == True:
        
            new_time = time.time()
            
            if first == True:
                print("Now sweeping...")
                #freqSweep(start=sweep[0],stop=sweep[1])
                first = False
                current_time = time.time()
            
            if current_time + wait_time < new_time:
                
                print("Freguency sweep from: " + str(sweep[0]) + " Hz to: " + str(sweep[1]) + " Hz with: " + str(volts[count]) + " V")

                first = True
                count += 1
                current_time = time.time()
                
                
                if count == 3:#change tihs to len(volt)
                    
                    doing_sweeps = False
                    move = True
                    count = 0

                
        ### moving to next position
        
        while move == True:
            
            if first == True:
                print("Now moving to next position...")
                MoveRelZ(move_length)
                current_time = time.time()
                first = False
                
            
            new_time = time.time()
              
        
            if current_time + wait_time < new_time:
                position[2] = PositionZ()
                print("Now in next position")
                run_count -= 1
                
                #creating statements
                background = True
                first = True
                doing_volts = False
                doing_sweeps = False
                move = False
                
                print("there are " + str(run_count) + " left out of a total of " + str(runs))
                
    print("characterization of tube is done")
  
if __name__ == "__main__":
    # creating processes
    p1 = multiprocessing.Process(target=Video, args=(0, ))
    p2 = multiprocessing.Process(target=Thor, args=(0, ))
      
    # starting process 1
    p1.start()
    # starting process 2
    p2.start()
    
      
    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()
      
    # both processes finished
    print("Done!")