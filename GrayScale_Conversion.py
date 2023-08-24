#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 14:11:47 2023

@author: joakimpihl
"""

# Code for converting BGR to grayscale according to https://stackoverflow.com/questions/17615963/standard-rgb-to-grayscale-conversion and https://en.wikipedia.org/wiki/Grayscale
        
def grayConvert(image):
    
    b,g,r = image[:,:,0]/255, image[:,:,1]/255, image[:,:,2]/255
    b_const, g_const, r_const = 0.0722, 0.7152, 0.2126
    
    img = b*b_const + g*g_const + r*r_const
    
    img[img<=0.0031308] = img[img<=0.0031308]*12.92
    img[img>0.0031308] = 1.055*img[img>0.0031308]**(1/2.4)-0.055
    
    
    return img
