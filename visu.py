import os
import numpy as np
import matplotlib.pyplot as plt
import measurement

def errorbar_latency(sizes, means, stds):
    '''Errorbar plot of the communication latency
    @param[in]  sizes   list of the sent data sizes
    @param[in]  means   array holding the mean for each size in [us]
    @param[in]  stds    array holding the standard deviation for each size
        in [us]'''
    plt.figure()
    plt.title('Latency of the communication')
    plt.errorbar(sizes, means, yerr=stds, fmt='o--g', capsize=5)
    plt.grid()
    plt.ylabel('Total latency [us]')
    plt.xlabel('Sent data size [byte]')


def errorbar_data_rate(sizes, means, stds):
    '''Errorbar plot of the communication data rate'''
    plt.figure()
    plt.title('Data rate of the communication')
    plt.errorbar(sizes, means, yerr=stds, fmt='o--g', capsize=3)
    plt.grid()
    plt.ylabel('Average data rate [byte/s]')
    plt.xlabel('Sent data size [byte]')

def histogram_latency_unique(sizes, all_latencies, indices):
    '''Histograms to display distribution of latencies
    @param[in]  sizes   list of all measurement data sizes in bytes
    @param[in]  all_latencies   np.array containing the meas values 
                                [sizes, meas_length]
    @param[in]  indices list of indices to plot the histogram of'''
    # Histogram with a seperate bin for each unique value
    n_subplots = len(indices)
    rows = int(np.floor(np.sqrt(n_subplots)))
    cols = int(np.ceil(n_subplots / rows))
    plt.figure()
    plt.suptitle('Histograms of all latencies')
    for i, index in enumerate(indices):
        plt.subplot(rows, cols, i+1)
        plt.title(f'{sizes[index]} bytes sent, total {all_latencies.shape[1]} measurement')
        bins = 256
        plt.hist(all_latencies[index], bins=bins)
        plt.grid()

def main():
    '''Reading in measurements, calculating mean, std then visualizing'''
    sizes = [16*x for x in range(17)] # [2048*x for x in range(17)]
    sizes[0] = 1
    clock = 240*1e6 # Hz
    dir_prefix = 'meas_480_240'

    all_meas_values = np.array(measurement.read_meas_from_files(sizes, dir_prefix))
    means = np.mean(all_meas_values, axis=1)
    stds = np.std(all_meas_values, axis=1)

    all_latencies = all_meas_values * 1e6 / clock # us
    latency_means = means * 1e6 / clock # us
    latency_stds = stds * 1e6 / clock # us
    errorbar_latency(sizes, latency_means, latency_stds)
    indices = [x for x in range(1, len(sizes), 4)] # histogram for half
    # indices = [len(sizes)-1]
    histogram_latency_unique(sizes, all_latencies, indices)

    min_data_rate = sizes / np.max(all_meas_values, axis=1) * clock # Byte/s
    max_data_rate = sizes / np.min(all_meas_values, axis=1) * clock # Byte/s
    data_rate_means = sizes / means * clock # Byte/s
    data_rate_p_errors = max_data_rate - data_rate_means # Byte/s
    data_rate_n_errors = data_rate_means - min_data_rate # Byte/s
    data_rate_errors = np.stack((data_rate_n_errors, data_rate_p_errors),
                                       axis=0)
    errorbar_data_rate(sizes, data_rate_means, data_rate_errors)
    # show graph
    plt.show()

if __name__ == '__main__':
    main()
