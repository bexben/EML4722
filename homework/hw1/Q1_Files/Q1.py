import numpy as np
import os
import subprocess
import pandas as pd

history_filename = '/home/bexben/school/CFD/homework/hw1/Q1_Files/history.csv'
cfg_filename = '/home/bexben/school/CFD/homework/hw1/Q1_Files/inv_NACA0012.cfg'
cfg_child_filename = '/home/bexben/school/CFD/homework/hw1/Q1_Files/inv_NACA0012_child.cfg'

variable = 'AOA' # variable to be edited
var_range = np.linspace(0, 15, 16) # values to test


def edit_line(variable, var_value) -> int:
    varlen = len(variable)
    num_edits = 0

    cfg_file = open(cfg_filename, 'r')
    cfg_list = cfg_file.readlines()
    cfg_file.close()
    # os.remove(cfg)

    for index, element in enumerate(cfg_list):
        if element[:varlen] == variable:
            cfg_list[index] = variable + '=' + str(var_value)
            num_edits += 1

    with open(cfg_child_filename, 'w') as new_cfg:
        for line in cfg_list:
            new_cfg.write(str(line))
    
    return num_edits

'''
def log_output(variable, var_value):
    file = pd.read_csv(history_filename)
    last_line = file.iloc[-1].values


'''
def run_tests(variable, var_range):
    for index, var_value in enumerate(var_range):
        history_path_edited = history_filename[:-4] + '_' + variable + str(var_value)
        edit_line(variable, var_value) # First one must set the variable
        edit_line('CONV_FILENAME', history_path_edited)

        # now we must run the file
        output = subprocess.run(['SU2_CFD', cfg_child_filename], check=True, text=True)


def main():
    run_tests(variable, var_range)

if __name__ == "__main__":
    main()
