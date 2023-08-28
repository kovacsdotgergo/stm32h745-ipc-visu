import matplotlib.pyplot as plt
import numpy as np
import measurement

def errorbar_latency_3d(clocks, latencies, size, direction='s', title=True):
    '''3d errorbar plot for latencies
    @param[in]  clocks  list of clock tuples (m7, m4) [MHz]
    @param[in]  latencies   list of latency tuples (mean, min, max)
    @param[in]  size    measured message size
    '''
    # todo: size 1 problematic, tuples should be handled with zip, then np
    # calculating lower and upper error from min and max
    latencies = measurement.upper_lower_from_minmax(latencies)
    latencies = np.array(latencies).squeeze()
    mean = latencies[:, 0]
    err = latencies[:, (1, 2)].T
    m7, m4 = zip(*clocks)
    # plot the data with error bars
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.errorbar(m7, m4, mean, zerr=err, fmt='og')
    ax.set_xlabel('M7 core clock [MHz]')
    # ax.set_xticklabels([0, None, None, None, 400])
    ax.set_ylabel('M4 core clock [MHz]')
    # ax.set_yticklabels([0, None, None, None, 200])
    ax.set_zlabel('Latency mean, errorbar for min and max [us]')
    if title:
        dir_text = 'from M7 to M4' if 's' == direction else 'from M4 to M7'
        ax.set_title(f'Sending {size[0]} bytes {dir_text}')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)


def errorbar_datarate_3d(clocks, datarates, size, direction='s', title=True):
    '''3d errorbar plot for datarates
    @param[in]  clocks  list of clock tuples (m4, m7) [MHz]
    @param[in]  datarates   list of datarate tuples (mean, min, max)
    @param[in]  size    measured message size
    '''
    #todo: same problem with 1 size, needs more work
    # calculating lower and upper error from min and max
    datarates = measurement.upper_lower_from_minmax(datarates)
    datarates = np.array(datarates).squeeze()
    mean = datarates[:, 0]
    err = datarates[:, (1, 2)].T
    m7, m4 = zip(*clocks)
    # plot the data with error bars
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.errorbar(m7, m4, mean, zerr=err, fmt='og')
    ax.set_xlabel('M7 core clock [MHz]')
    # ax.set_xticklabels([0, None, None, None, 400])
    # ax.set_ylabel('M4 core clock [MHz]')
    ax.set_yticklabels([0, None, None, None, 200])
    # M stands for 1e6 in this case (Mega, not Mibi)
    ax.set_zlabel('Data rate mean, min and max [Mbyte/s]')
    if title:
        dir_text = 'from M7 to M4' if 's' == direction else 'from M4 to M7'
        ax.set_title(f'Sending {size[0]} bytes {dir_text}')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
    clocks = [(72, 72), (120, 120), (196, 98), (200, 200), (240, 120),
              (240, 240), (248, 62), (280, 140), (304, 152), (308, 77),
              ] # each greater than 40
    size = [256] # list for read_meas_from_files

    for direction in ['r', 's']:
        latencies = [] # for storing tuple (mean, min, max)
        datarates = [] # (mean, min, max)
        for m7, m4 in clocks:
            dir_prefix = f'meas_{direction}_{m7}_{m4}'
            # timer clock is always the same as the m4 core's clock
            latencies.append(measurement.get_latencies(m4, dir_prefix, size)) # us
            datarates.append(measurement.get_datarates(m4, dir_prefix, size)) # Mbyte/s

        errorbar_latency_3d(clocks, latencies, size, direction, title=False)
        errorbar_datarate_3d(clocks, datarates, size, direction, title=False)

    # show graph
    plt.show()

if __name__ == '__main__':
    main()