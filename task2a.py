#!/usr/bin/env python3
from control import *

if __name__ == "__main__":
    x = [20, -20, 20, -50, 20, 40]
    for i in range(len(x)):
        if x[i] > 0:
            straight_forwards(x[i]/CM_PER_ROT)
        else:
            straight_forwards(x[i]/CM_PER_ROT)
    m1.off()
    m2.off()