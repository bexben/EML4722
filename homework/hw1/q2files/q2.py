import numpy as np
import os
import subprocess
import pandas as pd

# TODO: use path inside pathlib library rather than this shit
history_filename = '/home/bexben/school/CFD/homework/hw1/q2files/iterations/history.csv'
cfg_filename = '/home/bexben/school/CFD/homework/hw1/q2files/inv_NACA0012.cfg'
cfg_child_filename = '/home/bexben/school/CFD/homework/hw1/q2files/inv_NACA0012_child.cfg'
flow_filename = '/home/bexben/school/CFD/homework/hw1/q2files/iterations/flow'

variable = 'MACH_NUMBER' # variable to be edited
# var_range = np.linspace(0, 15, 16) # values to test
var_range = [0.2, 0.5, 0.85, 1, 1.5]


def edit_line(variable_list, var_value_list) -> int:
    cfg_file = open(cfg_filename, 'r')
    cfg_list = cfg_file.readlines()
    cfg_file.close()
    num_edits = 0

    for varIndex, (variable, var_value) in enumerate(zip(variable_list, var_value_list)):
        varlen = len(variable)

        for index, element in enumerate(cfg_list):
            if element[:varlen] == variable:
                cfg_list[index] = variable + '=' + str(var_value)
                num_edits += 1

    with open(cfg_child_filename, 'w') as new_cfg:
        for line in cfg_list:
            new_cfg.write(str(line))
    
    return num_edits


def run_tests(variable, var_range):
    for index, var_value in enumerate(var_range):
        history_path_edited = history_filename[:-4] + '_' + variable + str(var_value*10)
        flow_filename_edited = flow_filename + '_' + variable + str(var_value*10)

        edits = edit_line([variable, 
                           'CONV_FILENAME', 
                           'VOLUME_FILENAME'], 
                           [var_value, 
                            history_path_edited, 
                            flow_filename_edited])

        print(edits, var_value)

        # now we must run the file
        output = subprocess.run(['SU2_CFD', cfg_child_filename], check=True, text=True)


def main():
    run_tests(variable, var_range)

if __name__ == "__main__":
    main()
