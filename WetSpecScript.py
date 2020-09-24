'''
Jeremy Kansas
CS 350
Final Project I
'''

#test

import grovepi
from time import sleep
import json
import math
from datetime import datetime
from pathlib import Path


# analog ports:
light_sensor = 0

# digital ports:
dht_sensor = 7
red_led = 2
green_led = 3
blue_led = 8

# value indicating the dht sensor is the blue version
sensor_type = 0

# setup ports
grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(dht_sensor, "INPUT")
grovepi.pinMode(red_led, "OUTPUT")
grovepi.pinMode(green_led, "OUTPUT")
grovepi.pinMode(blue_led, "OUTPUT")

# set reading frequency (every 30 minutes)
sleep_time = 30 * 60 # units are seconds

# name of json file to save data to
json_file_name = "WetSpecData.json"



# convert celcius to fahrenheit
def C_to_F(celcius):

    return celcius * 9.0/5.0 + 32


# append new reading to JSON file (or create new one if necessary)
def store_reading(temp, humidity):

    # easy way to make sure data file exists
    Path(json_file_name).touch()

    # write data to json file - note dashboard requires json file to be an array of [time, humidity] arrays
    with open(json_file_name, 'r+') as f:

        # first load existing data
        # attempt to parse as json
        try:
            data = json.load(f)
        # fails if file is empty, so create empty list
        except:
            data = []

        # add new data to the list
        data.append([temp, humidity])

        # reset pointer to start of file and dump json
        f.seek(0)
        json.dump(data, f)


# check if it is currently 'daytime hours'
def is_daytime():

    # get current hour
    hour = datetime.now().hour

    # (daytime defined here for the sake of the assignment as 8am to 8pm)
    return hour > 8 and hour < 20


# check if it is currently 'daylight conditions'
def is_daylight():

    daylight = True

    # set resistance threshold for daylight sensing
    threshold = 1000

    try:
        # read light sensor
        sensor_value = grovepi.analogRead(light_sensor)

    except IOError:
        print("\nIOError")

    # calculate resistance
    if sensor_value == 0:
        daylight = False
    else:
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        daylight = resistance < threshold

    return daylight



def get_reading():

    try:
        # Get reading
        [temp, humidity] = grovepi.dht(dht_sensor, sensor_type)

    except IOError:
        print("\nIOError")

    #if math.isnan(temp) == False and math.isnan(humidity) == False:
    '''not sure the best way to deal with NaN readings (unlikely as they may be)'''

    return C_to_F(temp), humidity


def update_leds():

    # start by resetting all leds
    grovepi.digitalWrite(red_led, 0)
    grovepi.digitalWrite(green_led, 0)
    grovepi.digitalWrite(blue_led, 0)

    #  green when temp >60 <85 and humid < 80
    #  blue when temp > 85 < 95 and humid < 80
    #  red when temp > 95
    #  green and blue  humid > 80

    if temp > 95:
        grovepi.digitalWrite(red_led, 1)

    if humidity > 80:
        grovepi.digitalWrite(green_led, 1)
        grovepi.digitalWrite(blue_led, 1)
    elif temp > 85 and temp < 95:
        grovepi.digitalWrite(blue_led, 1)
    elif temp > 60 and temp < 85:
        grovepi.digitalWrite(green_led, 1)



#           #
# MAIN LOOP #
#           #
while True:

    # put in try block so we can catch Ctrl-C exit and run cleanup code
    try:
        do_reading = True

        # do nothing if it's not 'daylight hours'
        if not is_daytime():
            print("no reading - invalid time")
            do_reading = False

        # do nothing if it's not 'daylight conditions'
        if not is_daylight():
            print("no reading - inadequate daylight")
            do_reading = False

        if do_reading:
            # otherwise get reading from dht sensor
            [temp, humidity] = get_reading()
            print("reading taken - temp: {}  humidity: {}".format(temp, humidity))

            # write reading to JSON
            store_reading(temp, humidity)
            print("data stored in {}".format(json_file_name))

            update_leds()

        sleep(sleep_time)


    # Ctrl-C will cause KeyboardInterrupt exception and break out of while loop to do cleanup code
    except:
        break

# cleanup
print("User exited. LEDs turning off...")
grovepi.digitalWrite(red_led, 0)
grovepi.digitalWrite(green_led, 0)
grovepi.digitalWrite(blue_led, 0)
