#!/usr/bin/env python3
import re
import serial
from datetime import datetime
from tof_utils import *
from camera import *


regex = r"^uart: (\d+)mm, i2c: (\d+)mm$"  # TODO: modify regex to x and y


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    going_thru = False
    measurements = []

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            dist = re.search(regex, line)

            if dist:
                x, y = int(dist.group(1)), int(dist.group(2))
                print(x,y)

                if is_object(x, y) and going_thru == False:  # starting
                    start_time = datetime.now()
                    serialnum = start_time.strftime('%Y%m%d%H%M%S')
                    going_thru = True
                    take_pic(serialnum)
                    # print("new obj")

                if not is_object(x, y) and going_thru == True:  # ending
                    end_time = datetime.now()
                    xs = [m[0] for m in measurements][:-1]
                    ys = [m[1] for m in measurements][:-1]
                    # print(f'xs: {xs}, ys: {ys}')
                    theThing = obj(get_est_x(xs), get_est_y(ys), get_est_z(start_time, end_time), serialID=serialnum)
                    print(theThing.serialID)
                    print(f"x: {theThing.x}, y: {theThing.y}, z: {theThing.z}, volumn: {theThing.volumn}")
                    log_json(theThing)

                    going_thru = False
                    measurements = []

                if going_thru:
                    measurements.append([x, y])
                
