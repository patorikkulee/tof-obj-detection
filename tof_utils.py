import os, re
from datetime import datetime
import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import json
from collections import Counter

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
        self.pic_path = f'pictures/{self.serialID}.jpg'
        self.volumn = round((self.x * self.y * self.z)/1000, 2)

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
CONVEYOR_DIST = 270 # mm
GATE_WIDTH = 190 # mm


# --- functions ---

def is_object(x, y):
    if x!=0 and y!=0:
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


def log_json(object):
    with open('logfile.json', 'r+') as f:
        log = json.load(f)

        log[object.serialID] = {}
        log[object.serialID]['x'] = object.x
        log[object.serialID]['y'] = object.y
        log[object.serialID]['z'] = object.z
        log[object.serialID]['volumn'] = object.volumn
        log[object.serialID]['size'] = object.size()
        log[object.serialID]['picture'] = object.pic_path

        f.seek(0)
        json.dump(log, f, indent=4)


def get_prev_3():
    with open('logfile.json', 'r+') as f:
        log = json.load(f)
        serialIDs = sorted(log, reverse=True)[1:4]

        prev3 = {i:log[i] for i in serialIDs}
        return prev3


def log_line(entries):
    objInfo = ''
    for i in entries:
        objInfo += '# ------------\n'
        objInfo += f'object ID: {i}\n'
        objInfo += f'length of x: {entries[i]["x"]}\n'
        objInfo += f'length of y: {entries[i]["y"]}\n'
        objInfo += f'length of z: {entries[i]["z"]}\n'
        objInfo += f'object volumn: {entries[i]["volumn"]}\n'
        objInfo += f'object size range: {entries[i]["size"]}\n\n'
    
    os.system(f'echo "{objInfo}" > logfile.txt')


def draw_distribution(att:str):
    with open('logfile.json', 'r') as f:
        log = json.load(f)
    
    data = np.array([log[serialID][att] for serialID in log])
    data = dict(Counter(data))
    vals = np.array(list(data.values()))
    labels = list(data.keys())
    print(vals, labels)

    plt.pie(vals, labels=labels, autopct='%1.1f%%')
    plt.title(f'Distribution of {att}')
    plt.savefig(f'piecharts/{att}.png')


if __name__ == "__main__":
    # write_log(x)
    # write_log(x)
    # log_json(x)
    draw_distribution('size')
    # log_line(get_latest_3())

