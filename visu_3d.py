import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import measurement

def errorbar_latency_3d(clocks, latencies, size):
    '''3d errorbar plot for latencies
    @param[in]  clocks  list of clock tuples (m7, m4) [MHz]
    @param[in]  latencies   list of latency tuples (mean, min, max)
    @param[in]  size    measured message size
    '''
    # todo: size 1 problematic, tuples should be handled with zip, then np
    loc_latencies = latencies.copy()
    # calculating lower and upper error from min and max
    measurement.upper_lower_from_minmax(loc_latencies)
    loc_latencies = np.array(loc_latencies).squeeze()
    mean = loc_latencies[:, 0]
    err = loc_latencies[:, (1, 2)].T
    m7, m4 = zip(*clocks)
    # plot the data with error bars
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.errorbar(m7, m4, mean, zerr=err, fmt='og')
    ax.set_xlabel('M7 core clock [MHz]')
    ax.set_ylabel('M4 core clock [MHz]')
    ax.set_zlabel('Latency mean, errorbar for min and max [us]')
    ax.set_title(f'Sending {size} bytes from M7 to M4')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)


def errorbar_datarate_3d(clocks, datarates, size):
    '''3d errorbar plot for datarates
    @param[in]  clocks  list of clock tuples (m4, m7) [MHz]
    @param[in]  datarates   list of datarate tuples (mean, min, max)
    @param[in]  size    measured message size
    '''
    #todo: same problem with 1 size, needs more work
    loc_datarates = datarates.copy()
    # calculating lower and upper error from min and max
    measurement.upper_lower_from_minmax(loc_datarates)
    loc_datarates = np.array(loc_datarates).squeeze()
    mean = loc_datarates[:, 0]
    err = loc_datarates[:, (1, 2)].T
    m7, m4 = zip(*clocks)
    # plot the data with error bars
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.errorbar(m7, m4, mean, zerr=err, fmt='og')
    ax.set_xlabel('M7 core clock [MHz]')
    ax.set_ylabel('M4 core clock [MHz]')
    # M stands for 1e6 in this case
    ax.set_zlabel('Datarate mean, errorbar for min and max [Mbyte/s]')
    ax.set_title(f'Sending {size} bytes from M7 to M4')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
    clocks = [(8, 8), (72, 72), (80, 10), (120, 30), (120, 120),\
              (160, 10), (192, 12), (196, 98), (200, 200), (216, 27),\
              (240, 240), (248, 62), (280, 140), (304, 152),\
              (308, 77), (320, 40), (332, 166), (376, 96),\
              (412, 206), (432, 27), (444, 111), (480, 240)]
    size = [256] # list for read_meas_from_files

    latencies = [] # for storing tuple (mean, min, max)
    datarates = [] # (mean, min, max)
    for m7, m4 in clocks:
        dir_prefix = f'meas_{m7}_{m4}'
        # timer clock is always the same as the m4 core's clock
        latencies.append(measurement.get_latencies(m4, dir_prefix, size)) # us
        datarates.append(measurement.get_datarates(m4, dir_prefix, size)) # Mbyte/s

    errorbar_latency_3d(clocks, latencies, size)
    errorbar_datarate_3d(clocks, datarates, size)

    # show graph
    plt.show()

if __name__ == '__main__':
    main()