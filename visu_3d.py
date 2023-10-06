import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import measurement
import visu_common
import linear_model

def errorbar_3dfull(clocks, data, size, meas_type, direction='s', 
                     mem_domain='D1', title=True, color='b'):
    '''3d errorbar plot for datarates, plots full 
    @param[in]  clocks  list of clock tuples (m4, m7) [MHz]
    @param[in]  datarates   list of datarate tuples (mean, min, max)
    @param[in]  size    measured message size
    '''
    #todo: same problem with 1 size, needs more work
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    errorbar_3d(clocks, data, ax, '', color)
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

def errorbar_3d(clocks, data, ax, label, color):
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
    return ax.errorbar(m7, m4, mean, zerr=err, 
                       label=label, fmt='o', color=color)

def setup_ax(ax, direction, meas_type, size):
    '''Sets up all annotation on the 3d plot'''
    ax.set_xlabel('M7 core clock [MHz]')
    ax.set_ylabel('M4 core clock [MHz]')
    zlabel = 'Datarate errorbar [Mbyte/s]' if \
            'datarate' == meas_type else \
            'Latency errorbar [us]'
    ax.set_zlabel(zlabel)
    dir_text = 'from M7 to M4' if 's' == direction else 'from M4 to M7'
    ax.set_title(f'{size[0]} bytes {dir_text}')
    ax.set_xlim([0, 480])
    ax.set_ylim([0, 240])
    ax.set_zlim(0)
    ax.legend()

def model_grid(m7, m4, pred, ax, color):
    '''3d plot without figure and annotation
    Grid for the clocks and using it for a wireframe for pred'''
    m4_grid, m7_grid = np.meshgrid(m4, m7)
    ax.plot_wireframe(m7_grid, m4_grid, pred, rstride=34, cstride=34,
                      color=color, zorder=2, linestyle='dashed')

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
    # clocks = [(72, 72), (120, 120), (196, 98), (200, 200), (240, 120),
    #         (240, 240), (248, 62), (280, 140), (304, 152), (308, 77),
    #         (332, 166), (376, 96), (412, 206), (444, 111), (480, 60),
    #         (480, 120), (480, 240)] # each greater than 40
   
    size = [256] # list for read_meas_from_files
    mems = visu_common.get_mems('.', r'D[0-9]')
    meas_type = 'latency'

    cmap = mpl.colormaps['tab10'].colors
    wire_alpha = 0.6
    wire_cmap = mpl.colors.to_rgba_array(cmap, wire_alpha)

    for direction in ['r', 's']:
        ax = plt.figure().add_subplot(111, projection='3d')
        for color_idx, mem in enumerate(mems):
            clocks = visu_common.get_clocks_in_folder(
                mem, prefix=f'meas_{direction}_', clock_lambda=lambda m7, m4: m4 >= 60)
            
            # Measured data
            data = np.ndarray((len(clocks), 3, len(size)))
            for i, (m7, m4) in enumerate(clocks):
                dir_prefix = os.path.join(mem, f'meas_{direction}_{m7}_{m4}')
                # timer clock is always the same as the m4 core's clock
                data[i] = measurement.get_and_calc_meas(m4, dir_prefix, size, meas_type)
            errorbar_3d(clocks, data, ax, mem, cmap[color_idx])
            
                # Predictions by the model
            model = linear_model.LinearModel('models.json', mem, direction)
            m7, m4, pred = model.get_grid_for_range(clocks, size, meas_type)
            model_grid(m7, m4, pred, ax, wire_cmap[color_idx])
        setup_ax(ax, direction, meas_type, size)
    # show graph
    plt.show()

if __name__ == '__main__':
    main()