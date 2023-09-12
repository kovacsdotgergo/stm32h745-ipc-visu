import matplotlib.pyplot as plt
import numpy as np
import measurement
import visu_common
import os

def errorbar_latency_3dfull(clocks, latencies, size, direction='s', 
                        mem_domain='D2', title=True):
    '''3d errorbar plot for latencies, plots full plot for one mem
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
        ax.set_title(f'Sending {size[0]} bytes {dir_text}, mem is in {mem_domain}')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)


def errorbar_datarate_3dfull(clocks, datarates, size, direction='s', 
                         mem_domain='D1', title=True):
    '''3d errorbar plot for datarates, plots full 
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
    ax.set_ylabel('M4 core clock [MHz]')
    # ax.set_yticklabels([0, None, None, None, 200])
    # M stands for 1e6 in this case (Mega, not Mibi)
    ax.set_zlabel('Data rate mean, min and max [Mbyte/s]')
    if title:
        dir_text = 'from M7 to M4' if 's' == direction else 'from M4 to M7'
        ax.set_title(f'Sending {size[0]} bytes {dir_text}, mem is in {mem_domain}')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
    clocks = [(72, 72), (120, 120), (196, 98), (200, 200), (240, 120),
            (240, 240), (248, 62), (280, 140), (304, 152), (308, 77),
            (332, 166), (376, 96), (412, 206), (444, 111), (480, 60),
            (480, 120), (480, 240)] # each greater than 40
    clocks = visu_common.get_clocks_in_folder('D2_icache', prefix=f'meas_r_')
   
    size = [256] # list for read_meas_from_files
    mems = ['D2', 'D2_icache']
    for mem in mems:
        for direction in ['r', 's']:
            latencies = [] # for storing tuple (mean, min, max)
            datarates = [] # (mean, min, max)
            for m7, m4 in clocks:
                dir_prefix = os.path.join(mem, f'meas_{direction}_{m7}_{m4}')
                # timer clock is always the same as the m4 core's clock
                latencies.append(measurement.get_latencies(m4, dir_prefix, size)) # us
                datarates.append(measurement.get_datarates(m4, dir_prefix, size)) # Mbyte/s

            # errorbar_latency_3d(clocks, latencies, size, direction, mem, title=True)
            errorbar_datarate_3dfull(clocks, datarates, size, direction, mem, title=True)

    # show graph
    plt.show()

if __name__ == '__main__':
    main()