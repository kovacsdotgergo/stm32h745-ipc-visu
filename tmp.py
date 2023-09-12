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
x, y, z = [2, 3, 4], [3, 4, 5], [6, 7, 8]
zerr = [0.2, 0.1, 0.1]
x1, y1, z1 = [1, 2, 3], [2, 3, 4], [5, 6, 7]
zerr1 = [0.1, 0.2, 0.1]

ax = plt.figure().add_subplot(projection='3d')
ax.set_title('a')
ax.set_xlim([0, 12])
ax.set_ylim([0, 13])
ax.set_zlim(0)
ax.errorbar(x, y, z, zerr=zerr, fmt='o', color='black', label='Pontok1')
plot = ax.errorbar(x1, y1, z1, zerr=zerr1, fmt='o', color='red')
plot[0].set_label('a')
ax.legend()
print(plot[0])


plt.show()
print('a')
