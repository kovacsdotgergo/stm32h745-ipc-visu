import measurement
import visu
import numpy as np
import matplotlib.pyplot as plt
import os
import regex

# dirs = os.listdir()
# print(dirs)
# for dir in [x for x in dirs if os.path.isdir(x)]:
#     parts = dir.split(sep='_')
#     if parts[0] == 'meas':
#         print(f'({parts[1]}, {parts[2]})')

# sizes_short = [1 if x==0 else 16*x for x in range(17)]
# sizes_long = [1 if x==0 else 1024*x for x in range(16)] + [512, 1536, 16380]
# sizes = sizes_long
# sizes.sort()

# print(sizes_short, sizes_long)
# dir = 'meas_s_60_60'
# if not os.path.exists(dir):
#     os.makedirs(dir)
# #print(sizes)
# # ret = measurement.get_datarates(120, 'meas_s_120_120', sizes) # tuple of list
# # list_of_tuples = measurement.upper_lower_from_minmax(list(zip(*ret)))
# # np_arr = np.array(list_of_tuples)
# # visu.errorbar_data_rate(sizes, np_arr[:, 0], np_arr[:, 1:2].transpose())
# # plt.show()
# # print('h')

dicts = [{'mem': 'D2', 'clk': (120, 120)}, {'mem': 'D2', 'clk': (120, 120)}]

import visu_common
visu_common.get_mems(os.curdir)