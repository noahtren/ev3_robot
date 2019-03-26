#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import time

# INITIALIZE
m1 = LargeMotor(OUTPUT_A)
m2 = LargeMotor(OUTPUT_B)

m1.degrees

g = GyroSensor(INPUT_1)
g_off = 0
l = Leds()
l.set_color('LEFT', 'AMBER')

s = Sound(); s.set_volume(100)

g_off = 0
f = open("data.txt", "w")
CM_PER_ROT = 21.375

right_start = True

# s.speak("Hello")

def accelerate(forwards, r):
    if forwards:
        for i in range(0, 25):
            if r:
                m1.on(-25*i/25)
                m2.on(-25*i/25)
            else:
                m2.on(-25*i/25)
                m1.on(-25*i/25)
            time.sleep(0.01)
    else:
        for i in range(0, 25):
            m1.on(25*i/25)
            m2.on(25*i/25)
            time.sleep(0.01)

def straight_forwards(rot):
    global right_start
    # Function for going forwards one time
    dist = rot * 360
    offset = m1.degrees
    accelerate(True, right_start)
    while m1.degrees > (offset - dist + 180):
        time.sleep(0.01)
    # decelerate according to a fixed 1/2 rotation displacement as the end is approached
    while m1.degrees > (offset - dist):
        if right_start:
            m1.on(-25+((1-abs(m1.degrees-offset+dist)/180)*20))
            m2.on(-25+((1-abs(m1.degrees-offset+dist)/180)*20))
        else:
            m2.on(-25+((1-abs(m1.degrees-offset+dist)/180)*20))
            m1.on(-25+((1-abs(m1.degrees-offset+dist)/180)*20))
        time.sleep(0.01)
        #print("m1:{} m2:{}".format(m1.degrees, m2.degrees))
    if right_start:
        m1.off()
        m2.off()
    else:
        m2.off()
        m1.off()
    if right_start:
        right_start = False
    else:
        right_start = True
def turn(degrees):
    global g_off
    if g_off == 0:
        g_off = g.angle
    else:
        g_off += degrees
    time.sleep(0.01)
    if degrees > 0:
        m1.on(-10)
        m2.on(10)
        while g.angle - g_off < degrees - 30:
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on(-10)
            m2.on(10)
        while g.angle - g_off < degrees:
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on(-10+(5*(g.angle-g_off)/degrees))
            m2.on(10-(5*(g.angle-g_off)/degrees))
    else:
        m1.on(10)
        m2.on(-10)
        while g.angle - g_off > degrees + 30:
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on(15)
            m2.on(-15)
        while g.angle - g_off > degrees:
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on((10-(5*(g.angle-g_off)/degrees)))
            m2.on((-10+(5*(g.angle-g_off)/degrees)))
    m1.off()
    m2.off()
    g_off = 0
    time.sleep(1)
'''
def old_turn(rot):
    dist = rot * 360
    offset = m1.degrees
    # DO THE STRAIGHT
    accelerate(True)
    while m1.degrees > (offset - dist + 180):
        time.sleep(0.01)
    while m1.degrees > (offset - dist):
        m1.on(-25+((1-abs(m1.degrees-offset+dist)/180)*20))
        m2.on(-25+((1-abs(m1.degrees-offset+dist)/180)*20))
        time.sleep(0.01)
    # DO THE TURN
    global g_off
    if g_off == 0:
        g_off = g.angle
    else:
        g_off += 199
    time.sleep(0.01)
    m1.on(-10)
    m2.on(10)
    while g.angle - g_off < 180:
        f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
        m1.on(round(-15+(5*(g.angle-g_off)/180)), 1)
        m2.on(round(15-(5*(g.angle-g_off)/180)), 1)
    m1.off()
    m2.off()
    # END TURN
'''