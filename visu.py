import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import measurement
import linear_model
import visu_common

def model_plot(sizes, data, m7, m4, mem, color, if_label=False):
    '''Plot for data in function of size, formatted for the model'''
    plt.plot(sizes, data, alpha=0.5, linestyle='dashed', color=color,
             label=(f'{mem}pred, {m7}, {m4}' if if_label else None))

def errorbars(configs, sizes, data, cmap, if_line=True):
    '''Errorbar plot for several clock frequency, latency mesaurement
    Inputs:
        configs     list of dicts containgin clk and mem pairs
        sizes       list of the sent data sizes
        latencies   array of lantencies (mean, neg_err, pos_err)
            for each clk and size [clocks, 3, sizes]
    
    Note: there's no plt.figure call, so it can be used with subplot'''
    for i, config in enumerate(configs):
        m7, m4 = config['clk']
        means = data[i][0]
        errors = data[i][1:]
        plt.errorbar(sizes, means, yerr=errors, fmt='o', capsize=5,\
                     label=f'{config["mem"]}, {m7}, {m4}', color=cmap[i])
        if if_line:
            plt.plot(sizes, means, alpha=0.5, color=cmap[i])

def setup_errorbars(meas_type, direction):
    '''Annotate errorbar plot'''
    dir_text = 'Sending from M7 to M4' if direction == 's' else 'Sending from M4 to M7'
    plt.title(dir_text)
    plt.ylim(0)
    plt.grid()
    plt.legend(title='Memory, M7, M4 clk [MHz]')
    unit = 'us' if meas_type == 'latency' else 'MB/s'
    plt.ylabel(f'{meas_type.capitalize()} [{unit}]')
    plt.xlabel('Data size [B]')

def final_size_func_foreach(configs, meas_type, direction, if_model=False,
                            size_lambda=lambda size: size < 260):
    '''Draws complete final plot for each config'''
    cmap = mpl.colormaps['tab10'].colors
    size_dir = f'{configs[0]["mem"]}/meas_r_{configs[0]["clk"][0]}_{configs[0]["clk"][1]}'
    # sizes = [1 if x==0 else 16*x for x in range(17)] # [2048*x for x in range(17)]
    sizes = sorted(visu_common.get_sizes(size_dir, size_lambda=size_lambda))
    if if_model:
        model = linear_model.LinearModel('models_long.json',
                                         configs[0]['mem'],
                                         direction)

    data = np.ndarray((len(configs), 3, len(sizes)))
    for i, config in enumerate(configs):
        mem, (m7, m4) = config['mem'], config['clk']
        dir = f'{mem}/meas_{direction}_{m7}_{m4}'
        data[i] = measurement.get_and_calc_meas(m4, dir, sizes, meas_type)
        if if_model:
            model.set_model(mem, direction)
            pred = model.get_output(m7, m4, sizes, meas_type)
            model_plot(sizes, pred, m7, m4, mem, cmap[i])
    data = measurement.upper_lower_from_minmax(data)
    errorbars(configs, sizes, data, cmap, if_line=(not if_model))
    setup_errorbars(meas_type, direction)

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
    cmap = mpl.colormaps['tab10'].colors
    configs = [{'mem': 'D2_idcache_mpu_ncacheable', 'clk': (480, 60)},\
               {'mem': 'D2_idcache_mpu_ncacheable', 'clk': (240, 60)},
               {'mem': 'D2_idcache_mpu_ncacheable', 'clk': (120, 60)},]
    configs = [{'mem': 'D2', 'clk': (480, 240)},\
               {'mem': 'D2_icache', 'clk': (480, 240)},\
               {'mem': 'D2_idcache_mpu_ncacheable', 'clk': (480, 240)},\
               {'mem': 'D1', 'clk': (480, 240)},
               {'mem': 'D1_idcache_mpu_ncacheable', 'clk': (480, 240)},
               {'mem': 'D3', 'clk': (480, 240)},
               {'mem': 'D3_idcache_mpu_ncacheable_release', 'clk': (480, 240)},
               {'mem': 'D3_idcache_mpu_ncacheable', 'clk': (480, 240)}]
    configs = [{'mem': 'D1_idcache_mpu_ncacheable', 'clk': (480, 60)},\
               {'mem': 'D2_idcache_mpu_ncacheable', 'clk': (480, 60)},
               {'mem': 'D3_idcache_mpu_ncacheable', 'clk': (480, 60)},]
    meas_type = 'latency'
    
    dir = f'{configs[0]["mem"]}/meas_r_{configs[0]["clk"][0]}_{configs[0]["clk"][1]}'
    # sizes = [1 if x==0 else 16*x for x in range(17)] # [2048*x for x in range(17)]
    sizes = sorted(visu_common.get_sizes(dir, size_lambda=lambda size: size < 260))

    for direction in ['r', 's']:
        data = np.ndarray((len(configs), 3, len(sizes)))
        for i, config in enumerate(configs):
            dir = f'{config["mem"]}/meas_{direction}_{config["clk"][0]}_{config["clk"][1]}'
            data[i] = measurement.get_and_calc_meas(config['clk'][1], dir, sizes, meas_type)
        data = measurement.upper_lower_from_minmax(data)
        plt.figure()
        errorbars(configs, sizes, data, cmap)
        setup_errorbars(meas_type, direction)

    # show graph
    plt.show()

if __name__ == '__main__':
    main()
