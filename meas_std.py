import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    Histogram for different message sizes in case of long measurements.
        - histogram for changing bin size in case of a long measurement
        - histogram for changing measurement length with fixed num of bins
        - plot of change in mean and std with changing meas length
        - histogram with a bin for a each unique value, long measurement
    """
    filenames = ['putty1_65536.log', 'putty16_65536.log',
                 'putty128_65536.log', 'putty256_65536.log']
    all_meas_values = []
    for long_meas_filename in filenames:
        # cutting the expected datasize from the filename
        buffer_len = int(long_meas_filename.split('_', maxsplit=1)[0][5:])

        cur_meas_values = []
        with open(long_meas_filename, 'r', encoding='ascii') as file:
            file.readline() # header
            file.readline() # s
            meas_length = int(file.readline()) # length of the measurement
            file.readline() # empty line
            read_buffer_len = int(file.readline())
            if read_buffer_len != buffer_len:
                print('Wrong buffer size')
            file.readline() # empty line, could be left out
            for line in file:
                line = line.strip() # strip line ending
                if line: # if not empty line
                    cur_meas_values.append(int(line))
        if len(cur_meas_values) != meas_length: # read data and expected length
            print('Wrong file len')
        all_meas_values.append(cur_meas_values)
    
    # Plotting different number of bins
    for meas_values, long_meas_filename in zip(all_meas_values, filenames):
        plot_bins = [32, 64, 128, 256]
        num_fig = len(plot_bins)
        rows = int(np.floor(np.sqrt(num_fig)))
        cols = int(np.ceil(num_fig / rows))
        plt.figure()
        plt.suptitle(long_meas_filename)
        for i, bin_size in enumerate(plot_bins):
            plt.subplot(rows, cols, i+1)
            plt.title(f'Num of bins: {bin_size}')
            plt.hist(meas_values, density=False, bins=bin_size, alpha=0.5, color='green')
            plt.grid()
    # Based on this plot for the 1 long measurement 32 bins are enough

    # Plotting different number of measurements
    for meas_values, long_meas_filename in zip(all_meas_values, filenames):
        plot_meas_lengths = [128, 256, 512, 1024, 4096, 65536]
        num_fig = len(plot_meas_lengths)
        rows = int(np.floor(np.sqrt(num_fig)))
        cols = int(np.ceil(num_fig / rows))
        plt.figure()
        plt.suptitle(long_meas_filename)
        for i, meas_len in enumerate(plot_meas_lengths):
            plt.subplot(rows, cols, i+1)
            plt.title(f'Num of meas: {meas_len}')
            plt.hist(meas_values[0:meas_len], density=False, bins=32, alpha=0.5, color='green')
            plt.grid()
    # 1024 samples seem ok

    # Plot for mean and std change when changing measurement length
    n_subplots = len(filenames)
    plt.figure()
    plt.suptitle('Mean and std with changing length of measurement')
    for i, (meas_values, long_meas_filename) in enumerate(zip(all_meas_values, filenames)):
        mean_meas_lengths = np.linspace(2**7, 2**16, num=64, dtype=int)
        means = [np.mean(meas_values[:x]) for x in mean_meas_lengths]
        stds = [np.std(meas_values[:x]) for x in mean_meas_lengths]
        plt.title(f'{long_meas_filename}, mean')
        plt.subplot(n_subplots, 2, 2*i+1)
        plt.plot(mean_meas_lengths, means)
        plt.grid()
        plt.title(f'{long_meas_filename}, std')
        plt.subplot(n_subplots, 2, 2*i+2)
        plt.plot(mean_meas_lengths, stds)
        plt.grid()

    # Histogram with a seperate bin for each unique value
    rows = int(np.floor(np.sqrt(n_subplots)))
    cols = int(np.ceil(n_subplots / rows))
    plt.figure()
    plt.suptitle('Histograms with bins for each unique value')
    for i, (meas_values, long_meas_filename) in enumerate(zip(all_meas_values, filenames)):
        plt.subplot(rows, cols, i+1)
        plt.title(f'{long_meas_filename}')
        plt.hist(meas_values, bins=np.unique(meas_values))
        plt.grid()

    # show graph
    plt.show()
    plt.close('all')

main()
