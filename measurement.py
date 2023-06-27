import os
import serial
import numpy as np

class SerialConfig:
    '''Class holding the data neccessary for the serial configuration'''
    def __init__(self, port, baud, bytesize, parity, stopbits) -> None:
        '''Constructor'''
        self.port = port
        self.baud = baud
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits

def measure(num_meas, sent_data_size, serial_config) -> list:
    '''Function for measuring sent_data_size bytes, sending num_meas times
    '''
    response = []
    # Set up the serial connection
    with serial.Serial(serial_config.port, serial_config.baud) as ser:
        # start char
        ser.write(b's')
        response.append(ser.readline())
        # number of measurement repetition
        string_to_send = f'{num_meas}\r'.encode('ascii')
        ser.write(string_to_send)
        response.append(ser.readline())
        # measured data size
        string_to_send = f'{sent_data_size}\r'.encode('ascii')
        ser.write(string_to_send)
        response.append(ser.readline())
        for _ in range(num_meas):
            response.append(ser.readline())
    return response

def write_meas_to_file(dir_prefix, sent_data_size, num_meas, response, timer_clock):
    '''Function for writing the measurement results similarly to putty
    @param[in]  timer_clock   timer clock frequency in MHz'''
    filename = f'meas{sent_data_size}.log'
    fullpath = os.path.join(dir_prefix, filename)
    MODE = 'wb' if os.path.exists(fullpath) else 'xb'
    with open(fullpath, MODE) as file:
        # header
        file.write(f'Measurement repeated {num_meas} times, measured sending ' \
                f'of {sent_data_size} bytes from M7 to M4, timer clock:' \
                f'{timer_clock} MHz\n'.encode('ascii'))
        file.writelines(response)
    print(f'written to {filename}')

def read_meas_from_files(sizes, dir_prefix,
                         filename_prefix='meas') -> list[list]:
    '''Read all files for the elements given in sizes
    Returns: a list of lists that contain all the measurement values'''
    filenames = [os.path.join(dir_prefix, f'{filename_prefix}{x}.log') for x in sizes]
    all_meas_values = []
    for i, filename in enumerate(filenames):
        # cutting the expected datasize from the filename
        buffer_len = sizes[i]

        cur_meas_values = []
        with open(filename, 'r', encoding='ascii') as file:
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
    return all_meas_values

def get_latencies(timer_clock, dir_prefix, sizes):
    '''Reads in measurement values (mean, min, max) and calculates
        latencies
    @param[in]  timer_clock timer clock frequency in [MHz]
    @param[in]  dir_prefix  name of the directory
    @param[in]  sizes    measured message sizes
    @returns mean, min, max [us]'''
    all_meas_values = np.array(read_meas_from_files(sizes, dir_prefix))
    latency_mean = np.mean(all_meas_values, axis=1) / timer_clock # us
    latency_min = np.min(all_meas_values, axis=1) / timer_clock # us
    latency_max = np.max(all_meas_values, axis=1) / timer_clock # us
    return latency_mean, latency_min, latency_max

def get_datarates(timer_clock, dir_prefix, sizes):
    '''Reads measurement values (mean, min, max) and calculates datarates
    @param[in]  timer_clock timer clock frequency in [MHz]
    @param[in]  dir_prefix  name of the directory
    @param[in]  sizes    measured message sizes
    @returns mean, min, max [Mbyte/s]'''
    all_meas_values = np.array(read_meas_from_files(sizes, dir_prefix))
    data_rate_min = sizes / np.max(all_meas_values, axis=1) * timer_clock # Mbyte/s
    data_rate_max = sizes / np.min(all_meas_values, axis=1) * timer_clock # Mbyte/s
    data_rate_mean = sizes / np.mean(all_meas_values, axis=1) * timer_clock # Mbyte/s
    return data_rate_mean, data_rate_min, data_rate_max

def get_all_latencies(clocks, sizes, meas_num=1024,\
                      dir_prefix_without_clk='meas_'):
    '''Reads all measurement values for each clk and size
    @param[in]  clocks  list of tuple of clks (m7, m4)
    @param[in]  sizes   list of sizes
    @param[in]  meas_num    number of measurements in each file
    @param[in]  dir_prefix_without_clk  dir prefix without the clks 
            e.g. meas_ in case of meas_72_72
    @returns    np.array() with size (len(clocks), len(sizes), num_meas)'''
    all_latencies = np.empty((0, len(sizes), meas_num))
    for m7, m4 in clocks:
        new_meas_values = np.array( \
            read_meas_from_files(sizes, f'{dir_prefix_without_clk}{m7}_{m4}'))
        new_meas_values = np.expand_dims(new_meas_values, axis=0)
        all_latencies = np.concatenate(
            (all_latencies, new_meas_values / m4), axis=0) #us
    return all_latencies

class MeasType:
    latency = 0
    datarate = 1

def get_each_for_clk(clocks, sizes, meas_type):
    '''
    @param[in]  clocks      array of clock pair tuples (m7, m4)
    @param[in]  sizes       list of sizes
    @param[in]  meas_type   Meas_type.latency or datarate, the calculated 
        value to return
        
    @returns    np.array with size [len(clocks), 3, len(sizes)]'''
    all_values = np.empty((0, 3, len(sizes)))
    for m7, m4 in clocks:
        dir_prefix = f'meas_{m7}_{m4}'
        if meas_type == MeasType.latency:
            new_values = get_latencies(m4, dir_prefix, sizes)
        elif meas_type == MeasType.datarate:
            new_values = get_datarates(m4, dir_prefix, sizes)
        new_values = upper_lower_from_minmax(list(zip(*new_values)))
        new_values = np.expand_dims(np.array(new_values).T, axis=0)
        all_values = np.concatenate((all_values, new_values), axis=0)
    return all_values

def upper_lower_from_minmax(list_of_tuples):
    '''calculating lower and upper error from min and max
    @param[in]  list    input list of (mean, min, max) tuples
            
    @returns    output list of (mean, lower_err, upper_err) tuples
    '''
    ret = []
    for (mean, min_v, max_v) in list_of_tuples:
        ret.append((mean, mean-min_v, max_v-mean))
    return ret

def main():
    '''Measuring for several different sizes, saving the result to file'''
    serial_config = SerialConfig('COM5', 115200, 8, 'N', 1)
    NUM_MEAS = 1024
    # sizes = [16*x for x in range(17)] # [2048*x for x in range(17)]
    # sizes.append(512)
    # sizes.append(4096)
    # sizes.append(16384)
    # sizes[0] = 1
    # sizes = [1 if x==0 else 16*x for x in range(17)]
    sizes = [1 if x==0 else 2048*x for x in range(16)] + [32760, 512, 1024, 1536]
    m7 = 120
    m4 = 120
    timer_clock = m4
    DIR_PREFIX = 'tmp_meas' #f'meas_{m7}_{m4}'
    for sent_data_size in sizes:
        print(f'measuring {sent_data_size} long data...')
        response = measure(NUM_MEAS, sent_data_size, serial_config)
        write_meas_to_file(DIR_PREFIX, sent_data_size, NUM_MEAS, response,
                           timer_clock)

if __name__ == '__main__':
    main()
