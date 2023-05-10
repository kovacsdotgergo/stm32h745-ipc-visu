import numpy as np
import matplotlib.pyplot as plt
import os

def generate_points():
    size = 16
    for _ in range(10):
        m7 = np.random.randint(0, 120+1, size) * 4
        div = np.random.randint(0, 5, size)
        m4 = m7 / 2**div
        clocks = list(zip(m7, m4))
        clocks.append((480, 240))
        clocks.append((72, 72))
        print(clocks)
        visu_points(clocks)


def make_dirs(clocks, filename_prefix='meas'):
    base_path = os.getcwd()
    for m4, m7 in clocks:
        dir_path = os.path.join(base_path, f'{filename_prefix}_{m7}_{m4}')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

def visu_points(clocks):
    m4 = [x for x, _ in clocks]
    m7 = [y for _, y in clocks]
    plt.figure()
    plt.plot(m4, m7, 'x')
    plt.figure()
    a = [x for x in range(len(m4))]
    b = sorted(m4)
    plt.plot(a, b, 'x')
    plt.figure()
    a = [x for x in range(len(m7))]
    b = sorted(m7)
    plt.plot(a, b, 'x')

def main():
    # clocks = [(428, 26.75), (332, 166.0), (184, 11.5), (376, 96),\
    #           (120, 30.0), (196, 98.0), (280, 140), (304, 152.0),\
    #             (156, 9.75), (56, 28.0), (76, 9.5), (444, 111.0), (240, 240),\
    #             (364, 45.5), (308, 77.0), (8, 8.0), (200, 200), (120, 120), \
    #             (480, 240), (72, 72), (410, 205), (250, 75), (320, 40)]
    clocks = [(8, 8), (72, 72), (192, 12), (216, 27),\
            (80, 10), (120, 30), (120, 120),\
            (160, 10), (192, 12), (196, 98), (200, 200),\
            (240, 240), (248, 62), (280, 140), (304, 152),\
            (308, 77), (320, 40), (332, 166), (376, 96),\
            (412, 206), (432, 27), (444, 111), (480, 240)]
    print(sorted(clocks))
    visu_points(clocks)
    plt.show()

    # make_dirs(clocks)

if __name__ == '__main__':
    main()
