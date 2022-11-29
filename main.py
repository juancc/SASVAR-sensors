"""
Run with sudo for NIR sensor

- Each measure is saved in the file with a unique id
- Id are progressive integers on the first data stored
- NIR data is stored: id;R;S;T;U;V on each line of the text file

JCA
"""
import os
from datetime import datetime

from sensors.AS7263 import take_single_measurement_with_led

SAVE_DIR = 'recordings'

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    # Creates text file for each session with datetime stamp as filename
    dateTimeObj = datetime.now()
    timestamp = dateTimeObj.strftime("%d-%b-%Y_%H-%M-%S.%f")
    
    save_path = os.path.join(SAVE_DIR, timestamp+'.txt')

    end = False if input('Press x to start') == 'x' else True
    if end : exit()
    print('Starting recording...')
    with open(save_path, "a") as f:
        i=0
        while not end:
            x = take_single_measurement_with_led()
            print('NIR-{}: R:{}, S:{}, T:{}, U:{}, V:{}'.format(i, x[0],x[1],x[2],x[3],x[4]))
            x.insert(0, i)
            f.write(';'.join([str(j) for j in x]))
            end = False if input('x to continue?') == x else True

            i+=1




if __name__ == '__main__': main()