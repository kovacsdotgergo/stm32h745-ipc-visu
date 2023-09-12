import matplotlib.pyplot as plt
import numpy as np
import measurement
import visu_common
import os

def errorbar_3dfull(clocks, data, size, meas_type, direction='s', 
                     mem_domain='D1', title=True):
    '''3d errorbar plot for datarates, plots full 
    @param[in]  clocks  list of clock tuples (m4, m7) [MHz]
    @param[in]  datarates   list of datarate tuples (mean, min, max)
    @param[in]  size    measured message size
    '''
    #todo: same problem with 1 size, needs more work
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    errorbar_3d(clocks, data, ax)
    ax.set_xlabel('M7 core clock [MHz]')
    # ax.set_xticklabels([0, None, None, None, 400])
    ax.set_ylabel('M4 core clock [MHz]')
    # ax.set_yticklabels([0, None, None, None, 200])
    # M stands for 1e6 in this case (Mega, not Mibi)
    zlabel = 'Datarate errorbar [Mbyte/s]' if \
             'datarate' == meas_type else \
             'Latency errorbar [us]'
    ax.set_zlabel(zlabel)
    if title:
        dir_text = 'from M7 to M4' if 's' == direction else 'from M4 to M7'
        ax.set_title(f'Sending {size[0]} bytes {dir_text}, mem is in {mem_domain}')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)

def errorbar_3d(clocks, data, ax):
    ''' 3d plot without figure and annotation
    Inputs:
    clocks: list of (m7, m4) clocks
    data: list of (mean, min, max) measurements
    ax: subplot ax'''
    data = measurement.upper_lower_from_minmax(data)
    data = data.squeeze()
    mean = data[:, 0]
    err = data[:, (1, 2)].T
    m7, m4 = zip(*clocks)
    # plot the data with error bars
    ax.errorbar(m7, m4, mean, zerr=err, fmt='og')

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
    clocks = [(72, 72), (120, 120), (196, 98), (200, 200), (240, 120),
            (240, 240), (248, 62), (280, 140), (304, 152), (308, 77),
            (332, 166), (376, 96), (412, 206), (444, 111), (480, 60),
            (480, 120), (480, 240)] # each greater than 40
   
    clocks = visu_common.get_clocks_in_folder('D2_icache', prefix=f'meas_r_')
    size = [256] # list for read_meas_from_files
    mems = ['D2', 'D2_icache']
    meas_type = 'datarate'

    for mem in mems:
        for direction in ['r', 's']:
            latencies = np.ndarray((len(clocks), 3, len(size)))
            datarates = np.ndarray((len(clocks), 3, len(size)))
            for i, (m7, m4) in enumerate(clocks):
                dir_prefix = os.path.join(mem, f'meas_{direction}_{m7}_{m4}')
                # timer clock is always the same as the m4 core's clock
                latencies[i] = measurement.get_latencies(m4, dir_prefix, size) # us
                datarates[i] = measurement.get_datarates(m4, dir_prefix, size) # Mbyte/s

            errorbar_3dfull(clocks, datarates, size, meas_type, direction, 
                            mem, title=True)

    # show graph
    plt.show()

if __name__ == '__main__':
    main()