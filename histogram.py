import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats as stats

import measurement
import visu_common

def histogram(raw_meas, title):
    'Draws a histogram of the input raw measurement data'
    plt.title(title)
    plt.xlabel('Latency in # of clk')
    plt.ylabel('Count')
    bins = np.arange(raw_meas.min(), raw_meas.max() + 2) - 0.5
    plt.hist(raw_meas, bins=bins, log=True, align='mid', label='measured data')
    plt.grid()
    plt.legend(loc='upper right')

def histogram_intervals(raw_meas, title, std_center=False):
    'Histogram with std and confidence interval for the chosen sample size'
    raw_meas = np.array(raw_meas)

    mean = np.mean(raw_meas)
    std = np.std(raw_meas)
    conf_int = stats.norm.interval(0.95, loc=mean, scale=std/np.sqrt(1024))
    
    d = 5
    if std_center:
        raw_meas = raw_meas[(mean-d*std < raw_meas) 
                            & (raw_meas < mean+d*std)] # removing outlier
    histogram(raw_meas, title)
    plt.axvline(mean, color='red', linestyle='-', label='Mean')
    plt.axvline(mean - std, color='green', linestyle='--', label='Mean ± Std')
    plt.axvline(mean + std, color='green', linestyle='--')
    plt.axvline(conf_int[0], color='purple', linestyle='-.', label='95% CI')
    plt.axvline(conf_int[1], color='purple', linestyle='-.')
    if std_center:
        plt.xlim(mean-d*std, mean+d*std)
    plt.ylim(0, 1e5)
    
    # checkign why only even
    print(title, std, (conf_int[1]-conf_int[0])/mean*100)
    print(np.unique(raw_meas))

# def get_raw_foreach(base_path, mems, directions, clocks_lambda, sizes_lambda)
#     mems = visu_common.get_mems('pilot')
#     for mem in mems:
#         dir_prefix = os.path.join('pilot', mem)

#         directions = ['s', 'r']
#         for direction in directions:
#             clocks = visu_common.get_clocks_in_folder(dir_prefix, prefix=f'meas_{direction}_')
#             for m7, m4 in clocks:
#                 measurement_folder = os.path.join(dir_prefix, f'meas_{direction}_{m7}_{m4}')
#                 sizes = [16380] #visu_common.get_sizes(measurement_folder)
#                 raw = measurement.read_meas_from_files(sizes, measurement_folder)

def main():
    'Main functions, that draws the histogram of the pilot measurements'
    mems = visu_common.get_mems('pilot')
    for mem in mems:
        dir_prefix = os.path.join('pilot', mem)

        directions = ['s', 'r']
        for direction in directions:
            clocks = visu_common.get_clocks_in_folder(dir_prefix, prefix=f'meas_{direction}_')
            for m7, m4 in clocks:
                measurement_folder = os.path.join(dir_prefix, f'meas_{direction}_{m7}_{m4}')
                sizes = [16380] #visu_common.get_sizes(measurement_folder)
                raw = measurement.read_meas_from_files(sizes, measurement_folder)

                # for raw_per_size, size in raw, sizes:
                plt.figure()
                title = f'data size:{sizes[0]}, mem: {mem},\n' \
                        f'M7: {m7}, M4: {m4}, direction:{direction}'
                histogram_intervals(raw, title)
    plt.show()

if __name__ == '__main__':
    main()
