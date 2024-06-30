"""
The following code is used to test the servos and their different positions. 
It also allows defining the pulse widths to use the full range of motion.
"""

from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

#Use before run this script the next command in shell "sudo pigpiod"
factory = PiGPIOFactory()

#Factor of correction in width pulse to use all angle avaible
correction = 0.45
minPW = (1-correction)/1000
maxPW = (2+correction)/1000 

#Time between move 1 grade
step_time = 0.025

#Configuration of all servos
servo1 = AngularServo(12, min_angle=-45, max_angle=45, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo2 = AngularServo(6, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo3 = AngularServo(13, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo4 = AngularServo(15, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo5 = AngularServo(16, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo6 = AngularServo(17, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)

#Initial angle
angulo1 = 0
angulo2 = 0
angulo3 = 0
angulo4 = 0
angulo5 = 0
angulo6 = 0

#Function to move all servos to initial position
def home():
    servo1.mid()
    servo2.mid()
    servo3.mid()
    servo4.mid()
    servo5.mid()
    servo6.mid()

#Function to move all servos to max position
def max():
    servo1.max()
    servo2.max()
    servo3.max()
    servo4.max()
    servo5.max()
    servo6.max()

#Function to move all servos to min position
def min():
    servo1.min()
    servo2.min()
    servo3.min()
    servo4.min()
    servo5.min()
    servo6.min()

#Function to test positions of all servos
def test():
    print("posicionando en minimo")
    min()
    sleep(3)

    print("posicionando en home")
    home()
    sleep(3)
    
    print("posicionando en maximo")
    max()
    sleep(3)

#Functions to control the move of every servo, save return the final position to use in anguloi
#To control the speed change the value of step_time
def Ctrl_servo1(posicion, angulo):
    while True:
        if abs(angulo) <= 45:
            if angulo < posicion:
                posicion -= 1
                print(posicion)
                servo1.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                print(posicion)
                servo1.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                print("Servo 1 en posicion")
                return(posicion)
        else:
            print("El angulo para este servo uno solo puede estar entre -45 a 45")
            break

def Ctrl_servo2(posicion, angulo):
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                print(posicion)
                servo2.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                print(posicion)
                servo2.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                print("Servo 2 en posicion")
                return(posicion)
        else:
            print("El angulo para este servo uno solo puede estar entre -90 a 90")
            break

def Ctrl_servo3(posicion, angulo):
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                print(posicion)
                servo3.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                print(posicion)
                servo3.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                print("Servo 3 en posicion")
                return(posicion)
        else:
            print("El angulo para este servo uno solo puede estar entre -90 a 90")
            break

def Ctrl_servo4(posicion, angulo):
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                print(posicion)
                servo4.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                print(posicion)
                servo4.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                print("Servo 4 en posicion")
                return(posicion)
        else:
            print("El angulo para este servo uno solo puede estar entre -90 a 90")
            break
        
def Ctrl_servo5(posicion, angulo):
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                print(posicion)
                servo5.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                print(posicion)
                servo5.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                print("Servo 5 en posicion")
                return(posicion)
        else:
            print("El angulo para este servo uno solo puede estar entre -90 a 90")
            break
        
def Ctrl_servo6(posicion, angulo):
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                print(posicion)
                servo6.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                print(posicion)
                servo6.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                print("Servo 6 en posicion")
                return(posicion)
        else:
            print("El angulo para este servo uno solo puede estar entre -90 a 90")
            break


while True:
    
    servo = int(input("Numero de servomotor: "))
    angulo = int(input("Posición: "))

    if servo == 1:
        print("Moviendo Servo1")
        angulo1 = Ctrl_servo1(angulo1, angulo)
    elif servo == 2:
        print("Moviendo Servo2")
        angulo2 = Ctrl_servo2(angulo2, angulo)
    elif servo == 3:
        print("Moviendo Servo3")
        angulo3 = Ctrl_servo3(angulo3, angulo)
    elif servo == 4:
        print("Moviendo Servo4")
        angulo4 = Ctrl_servo4(angulo4, angulo)
    elif servo == 5:
        print("Moviendo Servo5")
        angulo5 = Ctrl_servo5(angulo5, angulo)
    elif servo == 6:
        print("Moviendo Servo6")
        angulo6 = Ctrl_servo6(angulo6, angulo)
    else:
        print("El servo seleccionado no existe")
        