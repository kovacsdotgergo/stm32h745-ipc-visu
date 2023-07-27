import measurement
import visu
import numpy as np
import matplotlib.pyplot as plt
import os

dirs = os.listdir()
print(dirs)
for dir in [x for x in dirs if os.path.isdir(x)]:
    parts = dir.split(sep='_')
    if parts[0] == 'meas':
        print(f'({parts[1]}, {parts[2]})')

sizes =  [1 if x==0 else 2048*x for x in range(16)] + [512, 1024, 1536, 32760]
sizes.sort()

ret = measurement.get_datarates(120, 'tmp_meas', sizes) # tuple of list
list_of_tuples = measurement.upper_lower_from_minmax(list(zip(*ret)))
np_arr = np.array(list_of_tuples)
visu.errorbar_data_rate(sizes, np_arr[:, 0], np_arr[:, 1:2].transpose())
plt.show()
print('h')