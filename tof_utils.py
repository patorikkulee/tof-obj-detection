import os, re
from datetime import datetime
# import matplotlib.pyplot as plt
# import seaborn as sns
import json

"""
--- 說明 ---
x:閘門垂直
y:閘門水平
z:輸送帶方向
"""


class obj:
    def __init__(self, x=0, y=0, z=0, serialID=None):
        self.x = x
        self.y = y
        self.z = z
        self.serialID = serialID
        self.volumn = round((self.x * self.y * self.z)/1000, 2)
    
    # def volumn(self):
    #     vol_mm3 = self.x * self.y * self.z
    #     vol_cm3 = vol_mm3/1000
    #     return round(vol_cm3, 2)

    def size(self):
        assert self.volumn >= 0

        if self.volumn > 200:
            return 'large'
        elif self.volumn < 100:
            return 'small'
        else:
            return 'medium'


# --- constants ---

THRESHOLD = 6 # mm
SPEED = 20 # mm/s
CONVEYOR_DIST = 300 # mm
GATE_WIDTH = 160 # mm


# --- functions ---

def is_object(x, y):
    if CONVEYOR_DIST - x >= THRESHOLD or GATE_WIDTH - y >=THRESHOLD:
        return True
    return False

    # xs = [dists[0] for dists in window]
    # ys = [dists[1] for dists in window]

    # if all([CONVEYOR_DIST - x > THRESHOLD for x in xs]) or all([CONVEYOR_DIST - y > THRESHOLD for y in ys]):
    #     return True
    
    # return False


def get_est_x(xs:list):
    real_xs = [CONVEYOR_DIST - x for x in xs]
    avg_x = sum(real_xs)/len(real_xs)
    return round(avg_x, 2) # use mean as the estimated distance
    # return max(dists, key=dists.count) # use mode as the estimated distance


def get_est_y(ys:list):
    real_ys = [GATE_WIDTH - y for y in ys]
    avg_y = sum(real_ys)/len(real_ys)
    return round(avg_y, 2) # use mean as the estimated distance
    # return max(dists, key=dists.count) # use mode as the estimated distance


def get_est_z(start, end):
    elapsedTime = end - start
    elapsedTime = elapsedTime.total_seconds() # from timedelta to float
    len_z = elapsedTime * SPEED
    return round(len_z, 2)


def log_line(object):
    objInfo = '# ------------\n'
    objInfo += f'object ID: {object.serialID}\n'
    objInfo += f'length of x: {object.x}\n'
    objInfo += f'length of y: {object.y}\n'
    objInfo += f'length of z: {object.z}\n'
    objInfo += f'object volumn: {object.volumn}\n'
    objInfo += f'object size range: {object.size()}\n'

    os.system(f'echo "{objInfo}" >> logfile.txt')


def log_json(object):
    with open('logfile.json', 'r+') as f:
        log = json.load(f)

        log[object.serialID] = {}
        log[object.serialID]['x'] = object.x
        log[object.serialID]['y'] = object.y
        log[object.serialID]['z'] = object.z
        log[object.serialID]['volumn'] = object.volumn
        log[object.serialID]['size'] = object.size()
        log[object.serialID]['picture'] = f'pictures/{object.serialID}.jpg'

        f.seek(0)
        json.dump(log, f, indent=4)


# def get_latest_3(logfile:str):
#     regex = r'# ------------\n'
#     regex += r'object ID: (\d{12})\n'
#     regex += r'length of x: (\d+(?:\.\d+)?)\n'
#     regex += r'length of y: (\d+(?:\.\d+)?)\n'
#     regex += r'length of z: (\d+(?:\.\d+)?)\n'
#     regex += r'object volumn: (\d+(?:\.\d+)?)\n'
#     regex += r'object size range: (\w+))\n'

#     with open(logfile, 'r') as f:
#         log = f.readlines()


if __name__ == "__main__":
    x = obj(40,20,300,"us")
    print(x.volumn)
    print(x.size())
    # write_log(x)
    # write_log(x)
    log_json(x)

