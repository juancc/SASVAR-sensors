import time
import RPi.GPIO as GPIO

def initialInductive(pin):
    global GPIOpin 
    GPIOpin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIOpin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Finished Initiation")
    print(GPIOpin)

def detectMetal():
    state = False
    if(GPIOpin != -1):
        state = GPIO.input(GPIOpin)
    else:
        print("Please Initial Input Pin")
    return state

# test module
if __name__ == '__main__':
    pin = 17
    initialInductive(pin)
    while True:
        is_metal = detectMetal()
        print(is_metal)
        time.sleep(0.2)