import numpy as np
import matplotlib.pyplot as plt
import measurement

def errorbars_latency(clocks, sizes, latencies):
    '''Errorbar plot for several clock frequency, latency mesaurement
    @param[in]  clocks  list of tuples of clk freqs (m7, m4)
    @param[in]  sizes   list of the sent data sizes
    @param[in]  latencies   array of lantencies (mean, neg_err, pos_err)
            for each clk and size [clocks, 3, sizes]
    
    @note   there's no plt.figure call, so it can be used with subplot'''
    plt.title('Latency of the communication')
    for i, (m7, m4) in enumerate(clocks):
        means = latencies[i][0]
        errors = latencies[i][1:]
        plt.errorbar(sizes, means, yerr=errors, fmt='o--', capsize=5, \
                     label=f'{m7}, {m4}')
    plt.ylim(0)
    plt.grid()
    plt.legend(title='M7 and M4 clk [MHz]')
    plt.ylabel('Average latency (avg, min, max) [us]')
    plt.xlabel('Sent data size [byte]')

def errorbars_data_rate(clocks, sizes, datarates):
    '''Errorbar plot for several clock frequency, datarate measurement
    @param[in]  clocks  list of tuples of clk freqs (m7, m4)
    @param[in]  sizes   list of the sent data sizes
    @param[in]  latencies   array of datarates (mean, neg_err, pos_err)
            for each clk and size [clocks, 3, sizes]
    
    @note   there's no plt.figure call, so it can be used with subplot'''
    plt.title('Data rate of the communication')
    for i, (m7, m4) in enumerate(clocks):
        means = datarates[i][0]
        errors = datarates[i][1:]
        plt.errorbar(sizes, means, yerr=errors, fmt='o--', capsize=5, \
                     label=f'{m7}, {m4}')
    plt.ylim(0)
    plt.grid()
    plt.legend(title='M7 and M4 clk [MHz]')
    plt.ylabel('Data rate (avg, min, max) [Mbyte/s]')
    plt.xlabel('Sent data size [byte]')

def errorbar_latency(sizes, means, errors):
    '''Errorbar plot of the communication latency
    @param[in]  sizes   list of the sent data sizes
    @param[in]  means   array holding the mean for each size in [us]
    @param[in]  errors  arrays holding the negative and positive errors in
        that order [us]'''
    plt.figure()
    plt.title('Latency of the communication')
    plt.errorbar(sizes, means, yerr=errors, fmt='o--g', capsize=5)
    plt.ylim(0)
    plt.grid()
    plt.ylabel('Average, min and max latency [us]')
    plt.xlabel('Sent data size [byte]')

def errorbar_data_rate(sizes, means, errors):
    '''Errorbar plot of the communication data rate'''
    plt.figure()
    plt.title('Data rate of the communication')
    plt.errorbar(sizes, means, yerr=errors, fmt='o--g', capsize=5)
    plt.grid()
    plt.ylabel('Average, min and max data rate [byte/s]')
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
    meas_num = 1024 # can pass to get_all_latencies
    sizes = [1 if x==0 else 16*x for x in range(17)] # [2048*x for x in range(17)]
    clocks = [(248, 62), (72, 72), (444, 111), (280, 140), (240, 240), \
            (480, 240)]
    # plot with several variable clocks and simple plots
    datarates = measurement.get_each_for_clk(clocks, sizes,
                                             measurement.MeasType.datarate)
    latencies = measurement.get_each_for_clk(clocks, sizes,
                                             measurement.MeasType.latency)
    plt.figure()
    errorbars_latency(clocks, sizes, latencies)
    plt.figure()
    errorbars_data_rate(clocks, sizes, datarates)
    errorbar_latency(sizes, latencies[0][0], latencies[0][1:])
    errorbar_data_rate(sizes, datarates[0][0], datarates[0][1:])

    sizes_multidim = [[1 if x==0 else 16*x for x in range(17)],
                     [1 if x==0 else 2048*x for x in range(16)]+[32760]]
    sizes_multidim[1].insert(1, 256)
    clocks_multidim = [(480, 240), (480, 120), (480, 60)]
    # plot with changing only one frequency
    plt.figure()
    for i, _sizes in enumerate(sizes_multidim):
        datarates = measurement.get_each_for_clk(clocks_multidim, _sizes,
                                             measurement.MeasType.datarate)
        latencies = measurement.get_each_for_clk(clocks_multidim, _sizes,
                                             measurement.MeasType.latency)
        plt.subplot(2, len(sizes_multidim), i+1)
        errorbars_latency(clocks_multidim, _sizes, latencies)
        plt.subplot(2, len(sizes_multidim), 2+i+1)
        errorbars_data_rate(clocks_multidim, _sizes, datarates)

    # histogram data and plot
    hist_sizes = [16, 256, 4096, 16384]
    hist_clocks = [(240, 240)] #[(480, 240), (480, 120), (480, 60)]
    all_latencies = measurement.get_all_latencies(hist_clocks, hist_sizes, meas_num)
    histogram_latency(hist_clocks, hist_sizes, all_latencies)

    # show graph
    plt.show()

if __name__ == '__main__':
    main()
