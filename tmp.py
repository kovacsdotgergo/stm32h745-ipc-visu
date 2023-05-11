import measurement
import numpy as np
import matplotlib.pyplot as plt

# arr = np.array(measurement.get_latencies(72, 'meas_72_72', [1, 16, 32, 48]))

b = [1 if x==0 else 16*x for x in range(17)]
a = [1 if x==0 else 2048*x for x in range(17)]
print(a)
print(b)