#!/usr/bin/env python3
from control import *

if __name__ == "__main__":
    x = [20, 20, 20, "5", 20, 40]
    r = [90, -90, None, -90, -90, 180]
    fi = open("stuff.txt", "w")
    fi.write("The stuff: \n")
    fi.close()
    for i in range(len(x)):
        fi = open("stuff.txt", "a+")
        if type(x[i]) == str:
            time.sleep(int(x[i]))
        else:
            fi.write("I am going straight for {} cm\n".format(x[i]))
            straight_forwards(x[i]/CM_PER_ROT)
        if i < len(r):
            if r[i] != None:
                fi.write("I am going to turn for {} degrees\n".format(r[i]))
                turn(r[i])
        fi.close()
    m1.off()
    m2.off()