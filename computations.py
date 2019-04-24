import math

def law_of_cosines(a, b, c):
    """Returns the angle opposite of side c"""
    # a^2 = b^2 + c^2 - (2bc)cos(A)
    cos = ((a**2) + (b**2) - (c**2))/(2*a*b)
    return math.acos(cos)

def iGPS_math(a, c, d):
    """Returns the x and y coordinates relative to
    the origin, given radial distances a, c, and d"""
    if a == 0:
        return 6,-6
    if c == 0:
        return 6,114
    if d == 0:
        return 102,114
    C_TO_A = 120 # the absolute distance between tower C and tower A
    C_TO_D = 96 # the absolute distance between tower C and tower D
    _theta = law_of_cosines(a,C_TO_A,c)
    _lambda = law_of_cosines(d,C_TO_D,c)
    print(_lambda)
    x = (math.sin(_theta) * a) + 6
    y = 108 - math.sin(_lambda) * d + 6
    return round(x,3), round(y,3)

def test_cosines():
    a = 65.39
    c = 111.52
    d = 100.65
    print(iGPS_math(a, c, d))

if __name__ == "__main__":
    test_cosines()