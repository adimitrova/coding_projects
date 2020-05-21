import math

"""
Wheel diameter = (rim diameter) + (tire diameter * 2).
Wheel circumference = Wheel diameter * PI.
# circumference of circle (tire)
"""


def calc_circumference(radius=None, diameter=None):
    if not radius:
        c = math.pi * diameter
    else:
        c = 2 * math.pi * radius
    return math.ceil(c)


def bike_wheel_diameter(rim_size_mm, tire_size_mm):
    return rim_size_mm + (tire_size_mm * 2)


def calc_distance(circumference, time):
    """
    s = v * t
    """
    return circumference * time


def to_mm(inch):
    return round(inch * 25.4, 2)


def hedgehog_mode():
    """
    Wheel size: 10.5 inch = 266.7mm
    Circumference: 838
    Weight: 0.812 kg

    Wheel size: 12 inch = 304.8mm
    Circumference: 958
    Weight: 1.245 kg
    """

    wheel_size = float(input("Wheel size in inches: "))
    # wheel_size = 12.5
    wheel_size_mm = to_mm(wheel_size)
    print("Wheel size: {} inch = {}mm".format(wheel_size, wheel_size_mm))
    print("Circumference (enter this value in the bike computer): {}"
          .format(calc_circumference(diameter=wheel_size_mm)))


def bicycle_mode():
    diam_mode = int(input("press \'1\' to enter ISO format for rim diameter or \'2\' for size in inches: "))
    rim_diameter = -1

    if diam_mode == 1:
        rim_diameter = float(input("Rim ISO diameter (mm): "))
    elif diam_mode == 2:
        rim_diameter_inch = float(input("Rim diameter (inch): "))
        rim_diameter = to_mm(rim_diameter_inch)

    tire_diameter_mm = float(input("Tire diameter in (mm): "))

    # rim_ISO_diameter_mm = 635
    # tire_diameter_mm = 20
    wheel_diamater = bike_wheel_diameter(rim_size_mm=rim_diameter,
                                         tire_size_mm=tire_diameter_mm)
    # print(wheel_diamater)
    print(calc_circumference(diameter=wheel_diamater))

    """
    Wheel diameter = (rim diameter) + (tire diameter * 2).
    Wheel circumference = Wheel diameter * PI.
    """


def main():
    mode = int(input("Enter \'1\' for bike mode or \'2\' for hedgehog wheel mode: "))

    if mode == 1:
        print("======= bicycle mode =======")
        bicycle_mode()
    elif mode == 2:
        print("======= hedgehog wheel mode =======")
        hedgehog_mode()


if __name__ == '__main__':
    main()
