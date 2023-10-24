import os
import matplotlib.pyplot as plt

import measurement
import visu_common
import histogram
import visu_3d
import visu

def main():
    '''Printing and writing out all final plots'''
    # Histogram
    # mems = visu_common.get_mems('pilot')
    # for mem in mems:
    #     dir_prefix = os.path.join('pilot', mem)

    #     directions = ['s', 'r']
    #     for direction in directions:
    #         clocks = visu_common.get_clocks_in_folder(dir_prefix, prefix=f'meas_{direction}_')
    #         for m7, m4 in clocks:
    #             measurement_folder = os.path.join(dir_prefix, f'meas_{direction}_{m7}_{m4}')
    #             sizes = [16380] #visu_common.get_sizes(measurement_folder)
    #             raw = measurement.read_meas_from_files(sizes, measurement_folder)

    #             # for raw_per_size, size in raw, sizes:
    #             plt.figure()
    #             title = f'data size:{sizes[0]}, mem: {mem},\n' \
    #                     f'M7: {m7}, M4: {m4}, direction:{direction}'
    #             histogram.histogram_intervals(raw, title)
    
    # =====================================================================
    # size plot clock dependecy 
    configs_all = [[{'mem': 'D3', 'clk': (480, 60)},
                    {'mem': 'D3', 'clk': (240, 60)},
                    {'mem': 'D3', 'clk': (120, 60)},],
                   [{'mem': 'D3', 'clk': (240, 240)},
                    {'mem': 'D3', 'clk': (240, 120)},
                    {'mem': 'D3', 'clk': (240, 60)},],]
    filename_all = ['_clockm7_size.pdf', '_clockm4_size.pdf']
    for conf_idx, (configs, filename) in enumerate(zip(configs_all, filename_all)):
        for meas_type in ['latency', 'datarate']:
            i = 0
            plt.figure(figsize=(10, 9.5), layout='tight')
            for size_lambda in [lambda size: size<=256, lambda _: True]:
                for direction in ['r', 's']:
                    if meas_type == 'latency' and (i == 1 or i == 3):
                            ax = plt.subplot(221 + i, sharey=ax) # second col
                    else:
                            ax = plt.subplot(221 + i)
                    if meas_type == 'datarate':
                        lim_fst_row, lim_sec_row = (7, 15) if conf_idx==1 else (2.25, 5) # y limits
                        if i == 0 or i == 1: # first row
                            plt.ylim(0, lim_fst_row)
                        else:
                            plt.ylim(0, lim_sec_row)
                    visu.final_size_func_foreach(configs, meas_type, direction,
                                                size_lambda=size_lambda)
                    i = i + 1
            out = os.path.join('figures', meas_type + filename)
            if not os.path.exists(out):
                plt.savefig(out)

    # =====================================================================
    # 3d clock dependency base 
    size = 256
    mems = visu_common.get_mems('.', r'D3')
    filename = 'base_3d.pdf'
    i = 0
    fig = plt.figure(figsize=(10, 9.5), layout='tight')
    for meas_type in ['latency', 'datarate']:
        for direction in ['r', 's']:
            if i == 1 or i == 3:
                ax = fig.add_subplot(221 + i, projection='3d', sharez=ax)
            else:
                ax = fig.add_subplot(221 + i, projection='3d')
            visu_3d.final3d_foreach(size, mems, direction, ax, meas_type=meas_type, if_cut=True, stride=20)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)

    # =====================================================================
    # difference among the memories plot for function of size todo 
    configs = [{'mem': 'D1', 'clk': (240, 240)},
               {'mem': 'D2', 'clk': (240, 240)},
               {'mem': 'D3', 'clk': (240, 240)},]
    filename = 'mems_size.pdf'
    i = 0
    plt.figure(figsize=(10, 9.5), layout='tight')
    for size_lambda, meas_type in zip([lambda size: size<=256, lambda _: True],
                                      ['latency', 'datarate']):
        for direction in ['r', 's']:
            ax = plt.subplot(221 + i)
            if meas_type == 'latency':
                plt.ylim(0, 60)
            else:
                plt.ylim(0, 17)
            visu.final_size_func_foreach(configs, meas_type, direction,
                                        size_lambda=size_lambda)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)

    # =====================================================================
    # difference among the memories 3d
    size = 4096
    mems = visu_common.get_mems('.', r'D[0-9]')
    filename = 'memories_3d.pdf'
    i = 0
    fig = plt.figure(figsize=(10, 9.5), layout='tight')
    for meas_type in ['latency', 'datarate']:
        for direction in ['r', 's']:
            ax = fig.add_subplot(221 + i, projection='3d')
            if meas_type == 'latency':
                ax.set_zlim([0, 1400])
            else:
                ax.set_zlim([0, 17])
            visu_3d.final3d_foreach(
                    size, mems, direction, ax, meas_type=meas_type,
                    clock_lambda=(lambda m7, m4: m7%120==0 and m4%60==0),
                    if_cut=False)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)

    # =====================================================================
    # difference among the memories with icache and optimization (2d only)
    # todo
    # =====================================================================
    # difference among the memories with cache and mpu todo (2d and 3d) 
    size = 16380
    mems = visu_common.get_mems('.', r'D[0-9]_idcache_mpu_ncacheable')
    filename = 'memories_cache_3d.pdf'
    i = 0
    fig = plt.figure(figsize=(10, 9.5), layout='tight')
    for meas_type in ['latency', 'datarate']:
        for direction in ['r', 's']:
            ax = fig.add_subplot(221 + i, projection='3d')
            if meas_type == 'latency':
                ax.set_zlim([0, 5000])
            else:
                ax.set_zlim([0, 25])
            visu_3d.final3d_foreach(
                    size, mems, direction, ax, meas_type=meas_type,
                    clock_lambda=(lambda m7, m4: m7%120==0 and m4%60==0),
                    if_cut=False)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)

    # =====================================================================
    # for each memory the difference between all the options todo (2d only)
    configs = [{'mem': 'D1_idcache_mpu_ncacheable', 'clk': (480, 240)},
               {'mem': 'D2_idcache_mpu_ncacheable', 'clk': (480, 240)},
               {'mem': 'D3_idcache_mpu_ncacheable', 'clk': (480, 240)},
               {'mem': 'D1', 'clk': (480, 240)},
               {'mem': 'D2', 'clk': (480, 240)},
               {'mem': 'D3', 'clk': (480, 240)},]
    filename = 'all_mems_size.pdf'
    i = 0
    plt.figure(figsize=(10, 9.5), layout='tight')
    for size_lambda, meas_type in zip([lambda size: size<=512, lambda _: True],
                                      ['latency', 'datarate']):
        for direction in ['r', 's']:
            ax = plt.subplot(221 + i)
            if meas_type == 'latency':
                plt.ylim(0, 80)
            else:
                plt.ylim(0, 27)
            visu.final_size_func_foreach(configs, meas_type, direction,
                                        size_lambda=size_lambda)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)

    # show graph
    #plt.show()

if __name__ == '__main__':
    main()