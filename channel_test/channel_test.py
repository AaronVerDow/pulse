#!/usr/bin/python
import fastopc as opc
import numpy as np
import json
from optparse import OptionParser


parser = OptionParser()
parser.add_option("--host", dest="host", default="127.0.0.1",
                  help="hostname or IP of opc server")
parser.add_option("--port", dest="port", default="7890",
                  help="port for opc server")
parser.add_option("--config", dest="config", default="../ws281x-config.json",
                  help="ledscape config file")
(options, args) = parser.parse_args()


def get_led_count():
    data = json.load(open(options.config))
    count = {}
    count['ledsPerStrip'] = data['ledsPerStrip']
    count['usedStripCount'] = data['usedStripCount']
    count['total'] = data['ledsPerStrip']*data['usedStripCount']
    return count


def create_pixel_array(led_count):
    '''
    Return a blank array of pixels
    '''
    return np.zeros((led_count, 3), dtype=np.uint8)


# define colors
colors = [
    {"name": "red", "color": [255, 0, 0]},
    {"name": "yellow", "color": [255, 255, 0]},
    {"name": "green", "color": [0, 255, 0]},
    {"name": "cyan", "color": [0, 255, 255]},
    {"name": "blue", "color": [0, 0, 255]},
    {"name": "magenta", "color": [255, 0, 255]}
]
white = [128, 128, 128]

# how long to wait between writing updates to the LEDs
default_sleep = 1

# setup opc client for writing to the LEDs
client = opc.Client("%s:%s" % (options.host, options.port))

# create default view, split into sections by function
count = get_led_count()
pixels = create_pixel_array(count['total'])


def main():
    master_pointer = 0
    while 1:
        pixels[:] = white
        pointer = master_pointer
        print " "
        for color in colors:
            print "%s: %s" % (color['name'], pointer)
            start = pointer * count['ledsPerStrip']
            pointer = pointer + 1
            end = pointer * count['ledsPerStrip'] - 1
            pixels[start:end] = color['color']

        client.put_pixels(pixels, channel=0)
        master_pointer = master_pointer + 1
        user_input = raw_input()

        if user_input == '':
            continue

        try:
            new_pointer = int(user_input)
            if 0 <= new_pointer <= count['usedStripCount']:
                master_pointer = new_pointer
        except:
            print "Invalid input"


if __name__ == "__main__":
    main()
