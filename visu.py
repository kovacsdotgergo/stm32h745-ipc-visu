import numpy as np
import matplotlib.pyplot as plt
import measurement
import visu_common

def errorbars(configs, sizes, data, meas_type):
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
        plt.errorbar(sizes, means, yerr=errors, fmt='o--', capsize=5, \
                     label=f'{config["mem"]}, {m7}, {m4}')

def setup_errorbars(meas_type, direction):
    '''Annotate errorbar plot'''
    dir_text = 'M7 to M4' if direction == 's' else 'M4 to M7'
    plt.title(f'{meas_type} of the communication ({dir_text})')
    plt.ylim(0)
    plt.grid()
    plt.legend(title='M7 and M4 clk [MHz]')
    unit = 'us' if meas_type == 'latency' else 'Mbyte/s'
    plt.ylabel(f'{meas_type} (avg, min, max) [{unit}]')
    plt.xlabel('Sent data size [byte]')


def histogram_latency(clocks, sizes, all_latencies):
    '''Histograms to display distribution of latencies
    @param[in]  clocks  list of tuples (m7, m4) clocks in [MHz]
    @param[in]  sizes   list of all measurement data sizes in bytes
    @param[in]  all_latencies   np.array containing the meas values 
                                [sizes, meas_length]
    @param[in]  indices list of indices to plot the histogram of'''
    n_subplots = len(sizes)
    rows = int(np.floor(np.sqrt(n_subplots)))
    cols = int(np.ceil(n_subplots / rows))
    plt.figure()
    plt.suptitle('Histograms of all latencies')
    for i, size in enumerate(sizes):
        plt.subplot(rows, cols, i+1)
        plt.title(f'{size} bytes sent, total {all_latencies.shape[2]} measurement')
        plt.xlabel('Latency [us]')
        plt.ylabel('Count')
        bins = 256
        for j, (m7, m4) in enumerate(clocks):
            plt.hist(all_latencies[j][i][:], bins=bins, log=True,
                     label=f'{m7}, {m4}')
        plt.grid()
        plt.legend(loc='upper right', title='M7 and M4 clk [MHz]')

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
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
        errorbars(configs, sizes, data, meas_type)
        setup_errorbars(meas_type, direction)

    sizes_multidim = [[1 if x==0 else 16*x for x in range(17)],
                     [1 if x==0 else 2048*x for x in range(16)]+[32760]]
    sizes_multidim[1].insert(1, 256)
    configs_multidim = [{'mem': 'D2', 'clk': (480, 240)},
                        {'mem': 'D2', 'clk': (480, 120)},
                        {'mem': 'D2', 'clk': (480, 60)}]

    # # histogram data and plot
    # hist_sizes = [16, 256, 4096, 16384]
    # hist_clocks = [(240, 240)] #[(480, 240), (480, 120), (480, 60)]
    # all_latencies = measurement.get_all_latencies(hist_clocks, hist_sizes, meas_num)
    # histogram_latency(hist_clocks, hist_sizes, all_latencies)

    # show graph
    plt.show()

if __name__ == '__main__':
    main()
