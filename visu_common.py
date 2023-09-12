import os
import regex

def get_clocks_in_folder(folder_path, prefix='meas_s_'): 
    clocks = []
    p = regex.compile(pattern=prefix + r'([0-9]+)_([0-9]+)')
    for dir in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, dir)):
            match = p.match(dir)
            if match:
                clocks.append((int(match[1]), int(match[2])))
    return clocks