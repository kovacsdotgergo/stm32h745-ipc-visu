import os
import regex

def get_clocks_in_folder(folder_path, prefix='meas_s_',\
                         clock_lambda=lambda m7, m4: True):
    '''Returns the clocks in folder, matching the given prefix, lambda can
        be used to filter resulting clks'''
    clocks = []
    pattern = regex.compile(pattern=prefix + r'([0-9]+)_([0-9]+)')
    for directory in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, directory)):
            match = pattern.match(directory)
            if match and clock_lambda(int(match[1]), int(match[2])):
                clocks.append((int(match[1]), int(match[2])))
    return clocks