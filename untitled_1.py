# Blob Detection and uart transport

import sensor, image, time, lcd

from pyb import UART
from pyb import delay

import json

# For color tracking to work really well you should ideally be in a very, very,

# very, controlled enviroment where the lighting is constant...

#green_threshold   =  (64, 97, -37, -11, 22, 66)
#orange_threshold   = (65, 100, 1, 30, 19, 73)
red_threshold  = (50, 76, 21, 71, -14, 63)
pink_threshold  =  (46, 93, 13, 68, -35, -2)
blue_threshold  =(72, 97, -47, -4, -22, -5)
black_threshold = (46, 92, 9, 42, -50, -2)
#green_threshold = (50, 91, -42, -8, -16, 11)
#purple_threshold   = (35, 88, 5, 37, -55, -19)
# You may need to tweak the above settings for tracking green things...

# Select an area in the Framebuffer to copy the color settings.
#(23, 60, -6, 16, 9, 48)

lcd.init()

sensor.reset() # Initialize the camera sensor.

sensor.set_pixformat(sensor.RGB565) # use RGB565.

sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.

sensor.skip_frames(10) # Let new settings take affect.

sensor.set_auto_whitebal(False) # turn this off.

clock = time.clock() # Tracks FPS.



uart = UART(3, 9600)

def find_max(blobs):

    max_size=0

    for blob in blobs:

        if blob.pixels() > max_size:

            max_blob=blob

            max_size = blob.pixels()
    return max_blob

def find_cy_min(blobs):

    cy_min=120

    for blob in blobs:

        if blob.cy() < cy_min:
            max_blob=blob
            cy_min = blob.cy()
    return max_blob


while(True):

    img = sensor.snapshot() # Take a picture and return the image.
    blobs = img.find_blobs([pink_threshold])
    if blobs:
        max_blob=find_cy_min(blobs)
        if max_blob.pixels() > 20:
            img.draw_rectangle(max_blob.rect())
            img.draw_cross(max_blob.cx(), max_blob.cy())
            lcd.display(img)
            output_str1="%d" % (max_blob.cx())
            output_str2="%d" % (max_blob.cy())
            output_str3="%d" % (max_blob.w())
            #output_str4="%d" % (max_blob.h())
       # uart.write(output_str)
      # UART.writechar(max_blob.cx())
       #UART.writechar(max_blob.cy())
            uart.write('x'+output_str1+'\r\n')
            uart.write('y'+output_str2+'\r\n')
            uart.write('z'+output_str3+'\r\n')
           # uart.write(output_str4+'\r\n')

            print('x')
            print(max_blob.cx())
            print('y')
            print(max_blob.cy())
            print('width')
            print(max_blob.w())
            print('height')
            print(max_blob.h())
            #print('size')
            #print(max_blob.pixels())


            delay(10)

        # uart.write(max_blob.cx())
        #uart.write(max_blob.cy())


    else:
        uart.write('n')
        #delay(10)
       # print('n')
