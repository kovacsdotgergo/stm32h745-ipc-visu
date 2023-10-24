import os
import matplotlib.pyplot as plt

import measurement
import visu_common
import histogram
import visu_3d
import visu

def if_large_size(size):
    '''Fuction to return sizes for the long size plots'''
    return (size % 64) == 0 or size == 1

def if_small_size(size):
    '''Function to return sizes for the short size plots'''
    return size < 256

def main():
    '''Printing and writing out all final plots'''
    # =====================================================================
    # Histogram
    filename = 'histogram.pdf'
    mem = 'D3_idcache_mpu_ncacheable_release' #visu_common.get_mems('pilot', pattern=r'D3_.*')
    dir_prefix = os.path.join('pilot', mem)
    plt.figure(figsize=(10, 9.5), layout='tight')
    i = 0
    for direction in ['r', 's']:
        clocks = visu_common.get_clocks_in_folder(dir_prefix, prefix=f'meas_{direction}_')
        for m7, m4 in clocks:
            measurement_folder = os.path.join(dir_prefix, f'meas_{direction}_{m7}_{m4}')
            sizes = [16380] #visu_common.get_sizes(measurement_folder)
            raw = measurement.read_meas_from_files(sizes, measurement_folder)
            # for raw_per_size, size in raw, sizes:
            plt.subplot(221 + i)
            dir_txt = 'M7 to M4' if direction=='s' else 'M4 to M7'
            title = f'Size:{sizes[0]} B, M7: {m7} MHz, M4: {m4} MHz, {dir_txt}'
            histogram.histogram_intervals(raw, title)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)
    
    # =====================================================================
    # initial plot to show difference between release and debug, long and short latency and datarate
    configs = [{'mem': 'D3', 'clk': (240, 240)},
               {'mem': 'D3_idcache_mpu_ncacheable_release', 'clk': (240, 240)},
               {'mem': 'D3_idcache_mpu_ncacheable', 'clk': (240, 240)},]
    filename = 'release_and_length_size.pdf'
    direction = 's'
    i = 0
    plt.figure(figsize=(10, 9.5), layout='tight')
    for meas_type in ['latency', 'datarate']:
        for size_lambda in [if_small_size, if_large_size]:
            ax = plt.subplot(221 + i)
            # if meas_type == 'latency':
            #     plt.ylim(0, 60)
            # else:
            #     plt.ylim(0, 17)
            visu.final_size_func_foreach(configs, meas_type, direction,
                                        size_lambda=size_lambda)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)

    # =====================================================================
    # size plot clock dependecy 
    configs_all = [[{'mem': 'D3', 'clk': (480, 60)},
                    {'mem': 'D3', 'clk': (240, 60)},
                    {'mem': 'D3', 'clk': (120, 60)},],
                   [{'mem': 'D3', 'clk': (240, 240)},
                    {'mem': 'D3', 'clk': (240, 120)},
                    {'mem': 'D3', 'clk': (240, 60)},],]
    filename_all = ['clock_m7_size.pdf', 'clock_m4_size.pdf']
    for conf_idx, (configs, filename) in enumerate(zip(configs_all, filename_all)):
        i = 0
        plt.figure(figsize=(10, 9.5), layout='tight')
        for size_lambda, meas_type in zip([if_small_size, if_large_size],
                                          ['latency', 'datarate']):
            for direction in ['r', 's']:
                ax = plt.subplot(221 + i)
                if conf_idx == 0: # effect of m7 figure
                    if meas_type == 'latency':
                        plt.ylim(0, 150)
                    else:
                        plt.ylim(0, 5)
                else:
                    if meas_type == 'latency':
                        plt.ylim(0, 140)
                    else:
                        plt.ylim(0, 16)
                visu.final_size_func_foreach(configs, meas_type, direction,
                                            size_lambda=size_lambda)
                i = i + 1
        out = os.path.join('figures', filename)
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
            visu_3d.final3d_foreach(size, mems, direction, ax, 
                                    meas_type=meas_type, if_cut=True,
                                    stride=20)
            i = i + 1
    out = os.path.join('figures', filename)
    if not os.path.exists(out):
        plt.savefig(out)

    # =====================================================================
    # difference between the memories plot for function of size todo 
    configs = [{'mem': 'D1', 'clk': (240, 240)},
               {'mem': 'D2', 'clk': (240, 240)},
               {'mem': 'D3', 'clk': (240, 240)},]
    filename = 'mems_size.pdf'
    i = 0
    plt.figure(figsize=(10, 9.5), layout='tight')
    for size_lambda, meas_type in zip([if_small_size, if_large_size],
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
    # difference between the memories 3d
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
    # difference between all cache options for one memory
    # todo
    # =====================================================================
    # difference between the memories with cache and mpu
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
    for size_lambda, meas_type in zip([lambda size: size<=512, if_large_size],
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
    plt.show()

if __name__ == '__main__':
    main()
