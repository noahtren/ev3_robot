#!/usr/bin/env python3

import ev3dev2
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.motor import SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, ColorSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import time
from bob import bob, command_handler

# INITIALIZE
m1 = LargeMotor(OUTPUT_A)
m2 = LargeMotor(OUTPUT_B)
try:
    m4 = MediumMotor(OUTPUT_D)
except ev3dev2.DeviceNotFound:
    pass

g = GyroSensor(INPUT_1)
g_off = 0

u = UltrasonicSensor(INPUT_3)

c_exists = True
try:
    c = ColorSensor(INPUT_2)
    c.mode='COL-COLOR'
except ev3dev2.DeviceNotFound:
    c_exists = False
l = Leds()
l.set_color('LEFT', 'AMBER')

s = Sound(); s.set_volume(100)

g_off = 0
f = open("data.txt", "w")
CM_PER_ROT = 8.415 # 21.375 for cm

right_start = True

def color_map():
    if c_exists:
        if c.value() > 1:
            return "White"
        else:
            return "Black"
    else:
        return "No reading"

# s.speak("Hello")
def push_data(moar=""):
    f = open("bigDat.txt", "a+")
    f.write("Color: {}, Distance: {}, {}\n".format(color_map(), u.value(), moar))
    f.close()

def shimmer(x):
    x = int(x)
    for i in range(0, x):
        l.set_color('LEFT',(0,1))
        l.set_color('RIGHT',(1,0))
        time.sleep(0.025)
        l.set_color('RIGHT',(0,1))
        l.set_color('LEFT',(1,0))
        time.sleep(0.025)

def reset_motors():
    m1.off()
    m2.off()
    m4.off()

def accelerate(forwards, r):
    if forwards:
        for i in range(0, 25):
            if command_handler(bob.commands):
                return
            if r:
                m1.on(-25*i/25)
                m2.on(-25*i/25)
            else:
                m2.on(-25*i/25)
                m1.on(-25*i/25)
            time.sleep(0.005)
    else:
        for i in range(0, 25):
            if command_handler(bob.commands):
                reset_motors()
                return
            m1.on(25*i/25)
            m2.on(25*i/25)
            time.sleep(0.005)

def straight_forwards(cm):
    global right_start
    # Function for going forwards one time
    rot = cm / CM_PER_ROT
    dist = rot * 360
    offset = m1.degrees
    accelerate(True, right_start)
    while m1.degrees > (offset - dist + 180):
        if command_handler(bob.commands):
            reset_motors()
            return
        time.sleep(0.01)
    # decelerate according to a fixed 1/2 rotation displacement as the end is approached
    while m1.degrees > (offset - dist):
        if command_handler(bob.commands):
            reset_motors()
            return
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

def straight_backwards(cm):
    global right_start
    # Function for going forwards one time
    rot = (cm / CM_PER_ROT) * -1
    dist = rot * 360
    offset = m1.degrees
    accelerate(False, right_start)
    while m1.degrees < (offset - dist - 180):
        if command_handler(bob.commands):
            reset_motors()
            return
        time.sleep(0.01)
    # decelerate according to a fixed 1/2 rotation displacement as the end is approached
    while m1.degrees < (offset - dist):
        if command_handler(bob.commands):
            reset_motors()
            return
        if right_start:
            m1.on(25-((1-abs(m1.degrees-offset+dist)/180)*20))
            m2.on(25-((1-abs(m1.degrees-offset+dist)/180)*20))
        else:
            m2.on(25-((1-abs(m1.degrees-offset+dist)/180)*20))
            m1.on(25-((1-abs(m1.degrees-offset+dist)/180)*20))
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
            if command_handler(bob.commands):
                reset_motors()
                return
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on(-10)
            m2.on(10)
        while g.angle - g_off < degrees+8:
            if command_handler(bob.commands):
                reset_motors()
                return
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on(-10+(5*(g.angle-g_off)/degrees))
            m2.on(10-(5*(g.angle-g_off)/degrees))
    else:
        m1.on(10)
        m2.on(-10)
        while g.angle - g_off > degrees + 30:
            if command_handler(bob.commands):
                reset_motors()
                return
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on(15)
            m2.on(-15)
        while g.angle - g_off > degrees-8:
            if command_handler(bob.commands):
                reset_motors()
                return
            f.write("offset: {} angle: {} delta: {}\n".format(g_off, g.angle, g.angle - g_off))
            m1.on((10-(5*(g.angle-g_off)/degrees)))
            m2.on((-10+(5*(g.angle-g_off)/degrees)))
    m1.off()
    m2.off()
    g_off = 0
    time.sleep(1)

m4.reset()

def dance():
    global bob
    while True:
        m1.on(100)
        m2.on(-100)
        if command_handler(bob.commands):
            reset_motors()
            return
        time.sleep(0.5)
        m1.on(-100)
        m2.on(100)
        time.sleep(0.5)

def close_claw():
    m4.on(40)
    while m4.degrees < 0:
        if command_handler(bob.commands):
            reset_motors()
            return
        time.sleep(0.005)
    m4.off()

def open_claw():
    m4.on(-40)
    while m4.degrees > -1000:
        if command_handler(bob.commands):
            reset_motors()
            return
        time.sleep(0.005)
    m4.off()

def move_and_scan():
    """ Scans from a location that is right against the first barcode """
    global bob
    c.mode='COL-COLOR'
    f = open("bigDat.txt","w+")
    # clear data file
    i = 0; cols = []
    while len(cols) != 4:
        reset_motors()
        time.sleep(0.5)
        cols.append(color_map())
        if len(cols) == 4:
            break
        m1.on(-3)
        m2.on(-3)
        time.sleep(0.7)
    reset_motors()
    f = open("final.txt","w+")
    print(cols)
    for col in cols:
        f.write("{}\n".format(col))
    return cols

def turn_and_grab_box():
    cols = move_and_scan()
    turn(-90)
    open_claw()
    straight_backwards(30)

def explore_and_find_boxes():
    """ Start could be A, B, C, or D """
    global bob
    bob.commands.push("straight_forwards(36)")
    bob.commands.push("hold()")
    bob.commands.push("turn(-90)")
    bob.commands.push("hold()")
    bob.commands.push("straight_forwards(42)")
    bob.commands.push("hold()")
    bob.commands.push("turn(-90)")
    bob.commands.push("hold()")
    bob.commands.push("straight_forwards(30)")
    bob.commands.push("hold()")
    bob.commands.push("turn(-90)")
    bob.commands.push("hold()")
    bob.commands.push("straight_forwards(42)")

