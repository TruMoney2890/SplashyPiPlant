#!/usr/bin/python3
import RPi.GPIO as gpio
import gpiozero
import time
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

stops = 0
ENA = 18
ENB = 12
IN1 = 4
IN2 = 17
IN3 = 27
IN4 = 22
FORWARD = 1
BACKWARD = 0
LEFT = 2
RIGHT = 3
FTrigger = 24
FEcho = 23
RTrigger = 8
REcho = 25
Relay = 26
liquid = 13
RSensor = 5
LSensor = 6



def init():
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(ENA, gpio.OUT)
    gpio.setup(ENB, gpio.OUT)
    gpio.setup(IN1, gpio.OUT)
    gpio.setup(IN2, gpio.OUT)
    gpio.setup(IN3, gpio.OUT)
    gpio.setup(IN4, gpio.OUT)
    gpio.setup(FTrigger, gpio.OUT)
    gpio.setup(FEcho, gpio.IN)
    #gpio.setup(Relay, gpio.OUT)
    gpio.setup(liquid, gpio.IN)
    gpio.setup(RSensor, gpio.IN)
    gpio.setup(LSensor, gpio.IN)
    gpio.setup(RTrigger, gpio.OUT)
    gpio.setup(REcho, gpio.IN)

def forward(speed, seconds):
    init()
    gpio.output(IN1, gpio.HIGH)
    gpio.output(IN2, gpio.LOW)
    gpio.output(IN3, gpio.HIGH)
    gpio.output(IN4, gpio.LOW)
    pwmA = gpio.PWM(ENA, 1000)
    pwmB = gpio.PWM(ENB, 1000)
    pwmA.start(speed)
    pwmA.start(speed)
    sleep(seconds)
    # gpio.cleanup()


def move(direction, speed, seconds):
    # init()

    if (direction == FORWARD):
        gpio.output(IN1, 0)  # Right Side Back
        gpio.output(IN2, 1)  # Right Side Forward
        gpio.output(IN3, 1)  # Left Side Forward
        gpio.output(IN4, 0)  # Left Side Back

    else:
        gpio.output(IN1, 1)  # Right Side Back
        gpio.output(IN2, 0)  # Right Side Forward
        gpio.output(IN3, 0)  # Left Side Forward
        gpio.output(IN4, 1)  # Left Side Back

    # pwmA = gpio.PWM(ENA, 1000)
    # pwmB = gpio.PWM(ENB, 1000)
    pwmA.start(speed)
    pwmB.start(speed)
    # sleep(seconds)
    # gpio.cleanup()


def stop():
    # init()
    gpio.output(IN1, 0)
    gpio.output(IN2, 0)
    gpio.output(IN3, 0)
    gpio.output(IN4, 0)
    # gpio.cleanup()


def pivot(direction, speed, seconds):
    # init()
    if direction == LEFT:
        gpio.output(IN1, 1)
        gpio.output(IN2, 0)
        gpio.output(IN3, 1)
        gpio.output(IN4, 0)

    else:  # Direction == RIGHT
        gpio.output(IN1, 0)
        gpio.output(IN2, 1)
        gpio.output(IN3, 0)
        gpio.output(IN4, 1)
    # pwmA = gpio.PWM(ENA, 1000)
    # pwmB = gpio.PWM(ENB, 1000)
    pwmA.start(speed)
    pwmB.start(speed)
    # sleep(seconds)
    # gpio.cleanup()


def moveStatus():
    #RSensor = gpiozero.DigitalInputDevice(5).is_active
    #LSensor = gpiozero.DigitalInputDevice(6).is_active
    if ( gpio.input(RSensor) == False) and ( gpio.input(LSensor) == False):
        return ('GO_STOP')
    if  gpio.input(RSensor) == False:
        return ('GO_LEFT')
    if  gpio.input(LSensor) == False:
        return ('GO_RIGHT')

    return ('GO_FORWARD')

def paststop():
    status = moveStatus()
    while(status == 'GO_STOP'):
        print('pass black line')
        move(FORWARD, 40, 0)
        time.sleep(.5)
        status = moveStatus()

def rpaststop():
    status = moveStatus()
    while(status == 'GO_STOP'):
        print('pass black line')
        move(BACKWARD, 40, 0)
        time.sleep(.5)
        status = moveStatus()

def Fdistance():
    gpio.output(FTrigger, True)
    time.sleep(0.0001)
    gpio.output(FTrigger, False)

    StartTime = time.time()
    StopTime = time.time()
    while gpio.input(FEcho) == 0:
        StartTime = time.time()

    while gpio.input(FEcho) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance

def Rdistance():
    gpio.output(RTrigger, True)
    time.sleep(0.0001)
    gpio.output(RTrigger, False)

    StartTime = time.time()
    StopTime = time.time()
    while gpio.input(REcho) == 0:
        StartTime = time.time()

    while gpio.input(REcho) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance


def water(ml):
    if(ml>=0):
        pumptime = ml/22
        gpio.setup(Relay, gpio.OUT)
        gpio.output(Relay, gpio.LOW)
        sleep(pumptime)
        gpio.cleanup(26)
        gpio.cleanup(Relay)

def test():
    init()
    gpio.output(IN1, gpio.HIGH)
    gpio.output(IN2, gpio.LOW)
    gpio.output(IN3, gpio.HIGH)
    gpio.output(IN4, gpio.LOW)
    sleep(5)
    gpio.cleanup()

def moveToNextLine():
    status = moveStatus()
    while (status != "GO_STOP"):
        dist = Fdistance()
        if (dist <= 10 and dist > 1):
            print ("Measured Distance = %.1f cm" % dist)
            stop()
            lcd.text("Object Detected", 1)
            lcd.text("Infront", 2)
        else:
            if (status == 'GO_FORWARD') :
               # print('Forward')
                move(FORWARD, 40, 0)
            elif (status == 'GO_LEFT') :
               # print('Left')
                pivot(LEFT, 60, 0)
            elif (status == 'GO_RIGHT') :
               # print('Right')
                pivot(RIGHT, 60, 0)
        status = moveStatus()
       # print('Status', status)
    stop()

def moveToPreviousLine():
    status = moveStatus()
    while(status != 'GO_STOP'):
        Rdist = Rdistance()
        if(Rdist <= 10):
            print ("Rear Measured Distance = %.1f cm" % Rdist)
            stop()
            lcd.text("Object Detected", 1)
            lcd.text("behind" , 2)
        else:
            if (status == 'GO_FORWARD') :
               # print('Back')
                move(BACKWARD, 40, 0)
            elif (status == 'GO_LEFT') :
                print('Left')
                pivot(RIGHT, 60, 0)
            elif (status == 'GO_RIGHT') :
                print('Right')
                pivot(LEFT, 60, 0)
        status = moveStatus()
    stop()


def getPlantName(position):
    #gets the name of the plant at the specified stop
    #need to limit how may characters are put on lcd screen
    pass

def getPlantWaterAmount():
    pass

def getPlantLocation():
    pass

def hasWater():
    if (gpio.input(liquid)):
        return True
    else:
        return False

if __name__ == '__main__':

    try:
        init()
        lcd = LCD()
        pwmA = gpio.PWM(ENA, 1000)
        pwmB = gpio.PWM(ENB, 1000)
        numberOfPlants = 3
        currentStop = 0
        backwardStop = 0
        watered = 0
        while (True):
            if hasWater():
                if (currentStop < numberOfPlants) and (watered != 1):
                    while(currentStop != 2):
                        paststop()
                        moveToNextLine()
                        currentStop +=1
                        plantName = getPlantName(currentStop)
                        lcd.text("Watering", 1)
                    #lcd.text(plantName, 2)
                        print("Watering")
                    #waterAmount = getPlantWaterAmount(currentStop)
                        water(88)
                    #lcd.clear()
                       # print('moving along',currentStop)
                    watered +=1
                elif (currentStop > 0) and (watered == 1):
                    lcd.text("Returning", 1)
                    lcd.text("to start", 2)
                    print('moving backwards ', currentStop)

                    while(currentStop != backwardStop):
                        print (currentStop != backwardStop)
                        #print("past stop", currentStop)
                        #rpaststop()
                        #print("previous line" , currentStop)
                        moveToPreviousLine()
                        #print('moving along',currentStop)
                        backwardStop +=1
                    print("sleep time")
                    time.sleep(5)
                    watered -=1


            else:
                lcd.text("Low Water", 1)
                stop()

    except KeyboardInterrupt:
        print("Program Stopping")
        gpio.cleanup()
        lcd.clear()

   # except Exception as e:
    #    print(e)

