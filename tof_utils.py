from datetime import datetime
import matpl

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
    
    def volumn(self):
        vol_mm = self.x * self.y * self.z
        vol_cm = vol_mm/1000
        return round(vol_cm, 2)


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
