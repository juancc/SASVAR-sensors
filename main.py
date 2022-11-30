"""
Run with sudo for NIR sensor

- Each measure is saved in the file with a unique id
- Id are progressive integers on the first data stored
- NIR data is stored: id;R;S;T;U;V on each line of the text file

JCA
"""
import sys

import os
from datetime import datetime

from sensors.AS7263 import take_single_measurement_with_led

# input function have different behaviours in Python 2 and 3
input_fn = input if sys.version_info[0] > 3 else raw_input

SAVE_DIR = 'recordings'

def main():
    if not os.path.exists(SAVE_DIR): # Work with Python 2.7
        os.makedirs(SAVE_DIR)

    # Creates text file for each session with datetime stamp as filename
    dateTimeObj = datetime.now()
    timestamp = dateTimeObj.strftime("%d-%b-%Y_%H-%M-%S.%f")
    
    save_path = os.path.join(SAVE_DIR, timestamp+'.txt')

    end = False if str(input_fn('Press Enter ')) == '' else True
    if end : exit()
    print('Starting recording...')
    with open(save_path, "a") as f:
        i=0
        while not end:
            x = take_single_measurement_with_led()
            print('NIR-{}: R:{}, S:{}, T:{}, U:{}, V:{}'.format(i, x[0],x[1],x[2],x[3],x[4]))
            x.insert(0, i)
            f.write(';'.join([str(j) for j in x])+'\n')

            end = False if input_fn('Another? (Press Enter)') == '' else True
            i+=1
    print('Total: {} records'.format(i))



if __name__ == '__main__': main()