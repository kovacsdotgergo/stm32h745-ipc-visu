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

sizes = [1 if x==0 else 2048*x for x in range(16)] + [32760]
ret = measurement.get_latencies(120, 'tmp_meas', sizes)
print(type(ret))
measurement.upper_lower_from_minmax()
visu.errorbar_latency(sizes, ret[0], ret[1:2])
plt.show()
print('h')