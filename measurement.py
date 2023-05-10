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

def read_meas_from_files(sizes, dir_prefix, filename_prefix='meas') -> list:
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

def get_latencies(timer_clock, dir_prefix, size):
    '''Reads in measurement values and calculates latencies
    @param[in]  timer_clock timer clock frequency in [MHz]
    @param[in]  dir_prefix  name of the directory
    @param[in]  size    measured message size
    @returns mean, min, max [us]'''
    all_meas_values = np.array(read_meas_from_files(size, dir_prefix))
    latency_mean = np.mean(all_meas_values, axis=1) / timer_clock # us
    latency_min = np.min(all_meas_values, axis=1) / timer_clock # us
    latency_max = np.max(all_meas_values, axis=1) / timer_clock # us
    return latency_mean, latency_min, latency_max

def get_datarates(timer_clock, dir_prefix, size):
    '''Reads measurement values and calculates datarates
    @param[in]  timer_clock timer clock frequency in [MHz]
    @param[in]  dir_prefix  name of the directory
    @param[in]  size    measured message size
    @returns mean, min, max [Mbyte/s]'''
    all_meas_values = np.array(read_meas_from_files(size, dir_prefix))
    data_rate_min = size / np.max(all_meas_values, axis=1) * timer_clock # Mbyte/s
    data_rate_max = size / np.min(all_meas_values, axis=1) * timer_clock # Mbyte/s
    data_rate_mean = size / np.mean(all_meas_values, axis=1) * timer_clock # Mbyte/s
    return data_rate_mean, data_rate_min, data_rate_max

def upper_lower_from_minmax(list_of_tuples):
    '''calculating lower and upper error from min and max
    @param[inout]  list    input list of (mean, min, max) tuples
            output list of (mean, lower_err, upper_err) tuples
    '''
    for i, (mean, min_v, max_v) in enumerate(list_of_tuples):
        list_of_tuples[i] = (mean, mean-min_v, max_v-mean)

def main():
    '''Measuring for several different sizes, saving the result to file'''
    serial_config = SerialConfig('COM5', 115200, 8, 'N', 1)
    NUM_MEAS = 1024
    sizes = [16*x for x in range(17)] # [2048*x for x in range(17)]
    sizes.append(512)
    sizes.append(4096)
    sizes.append(16384)
    sizes[0] = 1
    m7 = 444
    m4 = 111
    timer_clock = m4
    DIR_PREFIX = f'meas_{m7}_{m4}'
    for sent_data_size in sizes:
        print(f'measuring {sent_data_size} long data...')
        response = measure(NUM_MEAS, sent_data_size, serial_config)
        write_meas_to_file(DIR_PREFIX, sent_data_size, NUM_MEAS, response,
                           timer_clock)

if __name__ == '__main__':
    main()
