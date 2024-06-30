from color_detector import detect_color_in_photo
from gpiozero.pins.pigpio import PiGPIOFactory
from picamera2 import Picamera2, Preview
from comparation import comparison
from gpiozero import AngularServo
from colorama import Fore
from iir_filter import record_audio
import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import pygame
import cv2

try:
    GPIO.cleanup()
except:
    pass

#Use before run this script the next command in shell "sudo pigpiod"
factory = PiGPIOFactory()

#Factor of correction in width pulse to use all angle avaible
correction = 0.45
minPW = (1-correction)/1000
maxPW = (2+correction)/1000 

#Time between move 1 grade
step_time = 0.025
joystick_speed = 1

#Configuration of all servos
servo1 = AngularServo(14, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo2 = AngularServo(2,  min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo3 = AngularServo(3,  min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo4 = AngularServo(4,  min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo5 = AngularServo(17, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)
servo6 = AngularServo(27, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)

#Initial angle
angulo1 = 0
angulo2 = 28
angulo3 = -25
angulo4 = 0
angulo5 = 0
angulo6 = 0

#Angles to box position 1
a1 = 30
a2 = 80
a3 = -40
a4 = 0
a5 = 0
a6 = 0

#Angles to box position 2
b1 = 20
b2 = 90
b3 = -10
b4 = 0
b5 = 0
b6 = 0

#Angles to box position 3
c1 = 60
c2 = 80
c3 = -60
c4 = 0
c5 = 0
c6 = 0

#Angles to take position - where the element stand by
z1 = -10
z2 = 40
z3 = 10
z4 = -40
z5 = 0
z6 = 0

#Ranges of colors to use in camera
color_ranges = {
            # "Rojo": (np.array([0, 100, 100]), np.array([10, 255, 255])),
            # "Amarillo": (np.array([20, 100, 100]), np.array([30, 255, 255])),
            # "Verde": (np.array([50, 100, 100]), np.array([85, 255, 255]))
            
            # "Rojo": (np.array([0, 100, 100]), np.array([10, 255, 255])),
            # "Amarillo": (np.array([20, 50, 50]), np.array([30, 255, 255])),
            # "Verde": (np.array([50, 50, 50]), np.array([85, 255, 255]))

            "Rojo": (np.array([170, 100, 100]), np.array([179, 255, 255])),
            "Amarillo": (np.array([20, 50, 50]), np.array([30, 255, 255])),
            "Verde": (np.array([50, 50, 50]), np.array([85, 255, 255]))
            }

#Configuration of leds pins
GPIO.setmode(GPIO.BCM)

pin_rojo = 26
pin_verde = 23
pin_azul = 24

GPIO.setup(pin_rojo, GPIO.OUT)
GPIO.setup(pin_verde, GPIO.OUT)
GPIO.setup(pin_azul, GPIO.OUT)

#Function to turn on a led - use negative logic
def turn_on_led(pin):
    GPIO.output(pin, GPIO. LOW)

#Function to turn off a led - use negative logic
def turn_off_led(pin):
    GPIO.output(pin, GPIO. HIGH)

#Function to turn off all leds - use negative logic
def turn_off_leds():
    GPIO.output(pin_rojo, GPIO. HIGH)    
    GPIO.output(pin_verde, GPIO. HIGH)    
    GPIO.output(pin_azul, GPIO. HIGH)  

#Function to move all servos to initial position
def home(anguloa, angulob, anguloc, angulod, anguloe, angulof):
    angulo1 = Ctrl_servo1(anguloa, 0)
    angulo2 = Ctrl_servo2(angulob, 0)
    angulo3 = Ctrl_servo3(anguloc, 0)
    angulo4 = Ctrl_servo4(angulod, 0)
    angulo5 = Ctrl_servo5(anguloe, 0)
    angulo6 = Ctrl_servo6(angulof, 0)
    print(Fore.GREEN + "Robot posicionado en home" + Fore.WHITE)
    return angulo1, angulo2, angulo3, angulo4, angulo5, angulo6

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

#Posicionamiento de robot en determinada pose
def set_pose(theta1, theta2, theta3, theta4, theta5, theta6, angulo1, angulo2, angulo3, angulo4, angulo5, angulo6):
    angulo2 = Ctrl_servo2(angulo2, theta2)
    angulo3 = Ctrl_servo3(angulo3, theta3)
    angulo1 = Ctrl_servo1(angulo1, theta1)
    angulo4 = Ctrl_servo4(angulo4, theta4)
    angulo5 = Ctrl_servo5(angulo5, theta5)
    angulo6 = Ctrl_servo6(angulo6, theta6)
    Ver_pose(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)
    return angulo1, angulo2, angulo3, angulo4, angulo5, angulo6

#Function to test positions of all servos
def test():
    print("posicionando en minimo")
    min()
    sleep(3)

    print("posicionando en home")
    home(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)
    sleep(3)
    
    print("posicionando en maximo")
    max()
    sleep(3)

#Functions to control the move of every servo, save return the final position to use in anguloi
#To control the speed change the value of step_time
def Ctrl_servo1(posicion, angulo):
    # print("Moviendo Servo1")
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                servo1.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                servo1.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                return(posicion)
        else:
            print(Fore.RED + "El angulo para este servo uno solo puede estar entre -90 a 90")
            return(posicion)

def Ctrl_servo2(posicion, angulo):
    # print("Moviendo Servo2")
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                servo2.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                servo2.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                return(posicion)
        else:
            print(Fore.RED + "El angulo para este servo uno solo puede estar entre -90 a 90")
            return(posicion)

def Ctrl_servo3(posicion, angulo):
    # print("Moviendo Servo3")
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                servo3.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                servo3.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                return(posicion)
        else:
            print(Fore.RED + "El angulo para este servo uno solo puede estar entre -90 a 90")
            return(posicion)

def Ctrl_servo4(posicion, angulo):
    # print("Moviendo Servo4")
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                servo4.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                servo4.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                return(posicion)
        else:
            print(Fore.RED + "El angulo para este servo uno solo puede estar entre -90 a 90")
            return(posicion)
        
def Ctrl_servo5(posicion, angulo):
    # print("Moviendo Servo5")
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                servo5.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                servo5.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                return(posicion)
        else:
            print(Fore.RED + "El angulo para este servo uno solo puede estar entre -90 a 90")
            return(posicion)
        
def Ctrl_servo6(posicion, angulo):
    # print("Moviendo Servo6")
    while True:
        if abs(angulo) <= 90:
            if angulo < posicion:
                posicion -= 1
                servo6.angle = posicion
                sleep(step_time)
            elif angulo > posicion:
                posicion += 1
                servo6.angle = posicion
                sleep(step_time)
            elif posicion == angulo:
                return(posicion)
        else:
            print(Fore.RED + "El angulo para este servo uno solo puede estar entre -90 a 90")
            return(posicion)
        
def Ver_pose(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6):
    print("Angulo 1: " + Fore.GREEN + str(angulo1) + Fore.WHITE +"°")
    print("Angulo 2: " + Fore.GREEN + str(angulo2) + Fore.WHITE +"°")
    print("Angulo 3: " + Fore.GREEN + str(angulo3) + Fore.WHITE +"°")
    print("Angulo 4: " + Fore.GREEN + str(angulo4) + Fore.WHITE +"°")
    print("Angulo 5: " + Fore.GREEN + str(angulo5) + Fore.WHITE +"°")
    print("Angulo 6: " + Fore.GREEN + str(angulo6) + Fore.WHITE +"°")

#Set configuration of joystick
def Joystick_init():
    # Initialize pygame
    pygame.init()

    # Set up the joystick
    pygame.joystick.init()

    # Check for joystick presence
    if pygame.joystick.get_count() == 0:
        print(Fore.RED + "No se ha detectado ningun joystick.")
        exit()
    else:
        print(f"Joystick(s) {pygame.joystick.get_count()} detectados.")

    # Initialize the first joystick
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        servo_selected = 1
        print("Joystick Inicializado satisfactoriamente.")
        print("Parametros:.")
        print(f"Nombre: {joystick.get_name()}")
        print(f"Numero de ejes: {joystick.get_numaxes()}")
        print(f"Numero de botones: {joystick.get_numbuttons()}")
        print(f"Numero de hats: {joystick.get_numhats()}")
    except pygame.error:
        print("Error al inicializar el joystick.")
        exit()

        # Store previous axis values to detect changes
    previous_axis_values = [0] * joystick.get_numaxes()

    # Store previous button states to detect changes
    previous_button_states = [0] * joystick.get_numbuttons()

    # Store previous hat states to detect changes
    previous_hat_states = [0] * joystick.get_numhats()

    axis_counters = [0] * joystick.get_numaxes()
    hat_counters = [0] * joystick.get_numhats()

    return joystick, previous_axis_values, previous_button_states, previous_hat_states, servo_selected, axis_counters, hat_counters

#Create every counter
def update_counter(counter, value, speed):
    if -90 <= counter <= 90:
        new_counter = counter + (value*speed)
    else:
        new_counter = counter

    if round(new_counter) >= 91:
        new_counter = 90
    elif round(new_counter) <= -91:
        new_counter = -90

    return round(new_counter)

# #Function to take a photo an analize the predominant color
# def detect_color_in_photo(color_ranges):
#     try:
#         # Configurar la cámara
#         picam2 = Picamera2()
#         config = picam2.create_still_configuration(main={"format": "XRGB8888", "size": (640, 480)})
#         picam2.configure(config)
#         picam2.start()
        
#         # Esperar un momento para que la cámara se estabilice
#         sleep(2)
        
#         # Capturar una foto
#         frame = picam2.capture_array()
        
#         # Girar la imagen 180°
#         frame = cv2.rotate(frame, cv2.ROTATE_180)
        
#         # Convertir el frame a espacio de color HSV
#         hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
#         # Contadores de píxeles para cada color
#         color_counts = {color: 0 for color in color_ranges}
        
#         for color_name, (lower_color, upper_color) in color_ranges.items():
#             # Crear una máscara con el rango de colores especificado
#             mask = cv2.inRange(hsv_frame, lower_color, upper_color)
            
#             # Contar los píxeles de la máscara
#             color_counts[color_name] = cv2.countNonZero(mask)
            
#         # Determinar el color predominante
#         predominant_color = max(color_counts, key=color_counts.get)
#         if color_counts[predominant_color] == 0:
#             result = "No se ha detectado ningún color especificado"
#         else:
#             result = f"El color predominante es: {predominant_color}"
        
#         # Cerrar la cámara
#         picam2.stop()
#         picam2.close()
        
#         return result, predominant_color

#     except Exception as e:
#         return f"Error al intentar capturar la imagen: {str(e)}", None

turn_off_leds()

while True:
    print(Fore.YELLOW+"-----------------------------------------------------------------------------")
    try:
        opcion = int(input(Fore.WHITE +"Selecciona la accion a realizar: "+
                        "\n0. Informacion \n1. Automatico-Camara \n2. Audio \n3. Teclado \n4. Joystick \n5. Salir \n9. Ver pose \n"+
                        Fore.MAGENTA + "12. TEST \n"+  Fore.WHITE +   #Una vez ya no se hagan pruebas eliminar esta linea
                        "Numero de accion: " + Fore.GREEN))
        print(Fore.WHITE+"\n")
    except:
        opcion = 99
    
    #Banner de Informacion
    if opcion == 0:
        print(Fore.WHITE+
        " _____  _____    ______     ________ _____ _______ ____   \n"+
        "|  __ \|  __ \  / __ \ \   / /  ____/ ____|__   __/ __ \  \n"+
        "| |__) | |__)  | |  | \ \_/ /| |__ | |       | | | |  | | \n"+
        "|  ___/|  _  / | |  | |\   / |  __|| |       | | | |  | | \n"+
        "| |    | | \ \ | |__| | | |  | |___| |____   | | | |__| | \n"+
        "|_|___ |_|__\_\ \____/ _|_| _|______\_____|__|_|  \____/  \n"+
        "|  __ \  / __ \|  _ \ / __ \__   __|_   _/ ____|   /\     \n"+
        "| |__)  | |  | | |_) | |  | | | |    | || |       /  \    \n"+
        "|  _  / | |  | |  _ <| |  | | | |    | || |      / /\ \   \n"+
        "| | \ \ | |__| | |_) | |__| | | |   _| || |____ / ____ \  \n"+
        "|_|  \_\ \____/|____/_\____/ _|_| _|_____\_____/_/    \_\  \n"+
        " / ____/ __ \|  \/  | | || |                   \n"+
        "| |   | |  | | \  / | | || |_                  \n"+
        "| |   | |  | | |\/| | |__   _|                 \n"+
        "| |___| |__| | |  | |    | |                   \n"+
        " \_____\____/|_|  |_|    |_|                   \n"
                                                                                                                        
        )
        print(Fore.YELLOW+"-----------------------------------------------------------------------------")

        print(Fore.GREEN + "Opcion 0: " +
              Fore.WHITE + "Despliega este banner")

        print(Fore.GREEN + "Opcion 1: " +
              Fore.WHITE + "El robot determinara el color del elemento por medio de la camara y lo dejara en la posición previamente configurada.")

        print(Fore.GREEN + "Opcion 2: " +
              Fore.WHITE + "El robot determinara en que posición previamente configurada dejara el elemento en función del sonido escuchado.")

        print(Fore.GREEN + "Opcion 3: " +
              Fore.WHITE + "Permite controlar el robot de forma manual ingresando los angulos para cada uno de los motores.")
        
        print(Fore.GREEN + "Opcion 4: " +
              Fore.WHITE + "Permite controlar el robot de forma manual variando los angulos para cada uno de los motores por medio de un joystick.")

    #Programacion Automatica-Camara
    elif opcion == 1:
        #Determine the color of element
        result, predominant_color = detect_color_in_photo(color_ranges)
        print(result)

        #Take the element
        # angulo1, angulo2, angulo3, angulo4, angulo5, angulo6 = set_pose(z1, z2, z3, z4, z5, z6, angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)
        angulo4 = Ctrl_servo4(angulo4, -40)
        angulo1 = Ctrl_servo1(angulo1, z1)
        angulo2 = Ctrl_servo2(angulo2, z2)
        angulo3 = Ctrl_servo3(angulo3, z3)
        angulo4 = Ctrl_servo4(angulo4, 0)
        
        #Move element by colorself
        if predominant_color == "Rojo":
            turn_on_led(pin_rojo)
            turn_off_led(pin_verde)
            turn_off_led(pin_azul)
            # angulo1, angulo2, angulo3, angulo4, angulo5, angulo6 = set_pose(a1, a2, a3, a4, a5, a6, angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)
            
            angulo2 = Ctrl_servo2(angulo2, a2)
            angulo3 = Ctrl_servo3(angulo3, a3)
            angulo1 = Ctrl_servo1(angulo1, a1)
            angulo4 = Ctrl_servo4(angulo4, -40)
        elif predominant_color == "Verde":
            
            angulo2 = Ctrl_servo2(angulo2, b2)
            angulo3 = Ctrl_servo3(angulo3, b3)
            angulo1 = Ctrl_servo1(angulo1, b1)
            angulo4 = Ctrl_servo4(angulo4, -40)
            # angulo1, angulo2, angulo3, angulo4, angulo5, angulo6 = set_pose(b1, b2, b3, b4, b5, b6, angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)
        elif predominant_color == "Amarillo":
            
            angulo2 = Ctrl_servo2(angulo2, c2)
            angulo3 = Ctrl_servo3(angulo3, c3)
            angulo1 = Ctrl_servo1(angulo1, c1)
            angulo4 = Ctrl_servo4(angulo4, -40)
            # angulo1, angulo2, angulo3, angulo4, angulo5, angulo6 = set_pose(c1, c2, c3, c4, c5, c6, angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)
        else:
            turn_off_leds()

        angulo1, angulo2, angulo3, angulo4, angulo5, angulo6 = home(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)

    #Programacion Audio
    elif opcion == 2:
        record_audio()
        audio = comparison()
        Ver_pose(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)
        angulo4 = Ctrl_servo4(angulo4, -40)
        angulo1 = Ctrl_servo1(angulo1, z1)
        angulo2 = Ctrl_servo2(angulo2, z2)
        angulo3 = Ctrl_servo3(angulo3, z3)
        angulo4 = Ctrl_servo4(angulo4, 0)
        
        if audio == "Audio1":
            color_selected = "Rojo"
            print(Fore.GREEN + "Color seleccionado: " + color_selected + Fore.WHITE)
            angulo2 = Ctrl_servo2(angulo2, a2)
            angulo3 = Ctrl_servo3(angulo3, a3)
            angulo1 = Ctrl_servo1(angulo1, a1)
            angulo4 = Ctrl_servo4(angulo4, -40)
        elif audio == "Audio2":
            color_selected = "Verde"
            print(Fore.GREEN + "Color seleccionado: " + color_selected + Fore.WHITE)
            angulo2 = Ctrl_servo2(angulo2, b2)
            angulo3 = Ctrl_servo3(angulo3, b3)
            angulo1 = Ctrl_servo1(angulo1, b1)
            angulo4 = Ctrl_servo4(angulo4, -40)
        elif audio == "Audio3":
            color_selected = "Amarillo"
            print(Fore.GREEN + "Color seleccionado: " + color_selected + Fore.WHITE)
            angulo2 = Ctrl_servo2(angulo2, c2)
            angulo3 = Ctrl_servo3(angulo3, c3)
            angulo1 = Ctrl_servo1(angulo1, c1)
            angulo4 = Ctrl_servo4(angulo4, -40)
        else:
            color_selected = "Color no valido"
            print(Fore.RED + "Color seleccionado: " + color_selected + Fore.WHITE)

        angulo1, angulo2, angulo3, angulo4, angulo5, angulo6 = home(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)

    #Programación Control manual con teclado
    elif opcion == 3:
        print(Fore.GREEN + "Indique el numero de servomotor a manipular y la posicion en degradianes")
        print(Fore.GREEN + "Para regresar al menu principal seleccione el servomotor 9")

        while True:
            servo = int(input(Fore.WHITE + "Numero de servomotor: "))

            if servo != 9:
                angulo = int(input(Fore.WHITE + "Posición: "))

            if servo == 1:
                angulo1 = Ctrl_servo1(angulo1, angulo)
            elif servo == 2:
                angulo2 = Ctrl_servo2(angulo2, angulo)
            elif servo == 3:
                angulo3 = Ctrl_servo3(angulo3, angulo)
            elif servo == 4:
                angulo4 = Ctrl_servo4(angulo4, angulo)
            elif servo == 5:
                angulo5 = Ctrl_servo5(angulo5, angulo)
            elif servo == 6:
                angulo6 = Ctrl_servo6(angulo6, angulo)
            elif servo == 9:
                break    
            else:
                print(Fore.RED + "El servo seleccionado no existe")
                print(Fore.GREEN + "Indique el numero de servomotor a manipular y la posicion en degradianes")
                print(Fore.GREEN + "Para regresar al menu principal seleccione el servomotor 9 \n")
    
    #Programacion de Joystick
    elif opcion == 4:
        Use_joystick = True
        joystick, previous_axis_values, previous_button_states, previous_hat_states, servo_selected, axis_counters, hat_counters = Joystick_init()
        try:
            while Use_joystick:
                # Process pygame events
                pygame.event.pump()

                # Loop through all axes and print value if it changes
                # for i in range(joystick.get_numaxes()):
                #     axis_value = joystick.get_axis(i)
                #     if abs(axis_value) > 0.01:
                #         if i != 5:
                #             if i!= 2:
                #                 counter_increment = axis_value
                #                 axis_counters[i] = update_counter(axis_counters[i], counter_increment, joystick_speed)
                #                 print(f"Axis {i} value: {axis_value}, Counter: {axis_counters[i]}")
                                
                #                 if axis_counters[0] > 10:
                #                     axis_counters[0] = 10
                                    
                #                 # elif axis_counters[0] < 10:
                #                 #     axis_counters[0] = -10

                #                 # else:
                #                 #     pass

                #                 angulo1 = Ctrl_servo1(angulo1, axis_counters[0])
                #                 print(angulo1)
                #                 # angulo5 = Ctrl_servo2(angulo2, axis_counters[4])
                #         previous_axis_values[i] = axis_value
                    

                # Loop through all buttons and print value if it changes
                for i in range(joystick.get_numbuttons()):
                    button_state = joystick.get_button(i)
                    if button_state != previous_button_states[i]:
                        # print(f"Button {i} {'pressed' if button_state else 'released'}")    #Return int 0 or 1
                        previous_button_states[i] = button_state

                        if i== 4 and button_state == 1 and servo_selected > 1:
                            servo_selected -= 1 
                            print(Fore.GREEN + "Servo seleccionado: " + str(servo_selected) + Fore.WHITE)
                            if servo_selected == 1:
                                hat_counters[0] = angulo1
                            elif servo_selected == 2:
                                hat_counters[0] = angulo2
                            elif servo_selected == 3:
                                hat_counters[0] = angulo3
                            elif servo_selected == 4:
                                hat_counters[0] = angulo4
                            elif servo_selected == 5:
                                hat_counters[0] = angulo5
                            elif servo_selected == 6:
                                hat_counters[0] = angulo6

                        elif i== 5 and button_state == 1 and servo_selected < 6 :
                            servo_selected += 1 
                            print(Fore.GREEN + "Servo seleccionado: " + str(servo_selected) + Fore.WHITE)
                            if servo_selected == 1:
                                hat_counters[0] = angulo1
                            elif servo_selected == 2:
                                hat_counters[0] = angulo2
                            elif servo_selected == 3:
                                hat_counters[0] = angulo3
                            elif servo_selected == 4:
                                hat_counters[0] = angulo4
                            elif servo_selected == 5:
                                hat_counters[0] = angulo5
                            elif servo_selected == 6:
                                hat_counters[0] = angulo6

                        elif i == 6 and button_state == 1:
                            home(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)

                        elif i == 7 and button_state == 1:
                            Use_joystick = False

                # Loop through all hats (d-pads) and print value if it changes
                for i in range(joystick.get_numhats()):
                    hat_state = joystick.get_hat(i)
                    if hat_state != previous_hat_states[i]:
                        if hat_state[0] != 0:  # Horizontal direction
                            # joystick_speed = update_counter(speed_counters[i], 1, 1)
                            joystick_speed += hat_state[0]
                            print(Fore.WHITE + "La velocidad actual es de: " + Fore.GREEN + str(joystick_speed) + Fore.WHITE)
                        # print(f"Hat {i} value: {hat_state}")
                    if hat_state != (0, 0):  # If hat is not centered
                        if hat_state[1] != 0:  # Vertical direction
                            counter_increment = hat_state[1] * 1  # Increment proportional to time
                            hat_counters[i] = update_counter(hat_counters[i], counter_increment, joystick_speed)
                        # print(f"Hat {i} value: {hat_state}, Counter: {hat_counters[i]}")
                    previous_hat_states[i] = hat_state
                    # print(type(hat_counters[i]))

                    if servo_selected == 1:
                        angulo1 = Ctrl_servo1(angulo1, hat_counters[i])
                    elif servo_selected == 2:
                        # print("Moviendo Servo3")
                        angulo2 = Ctrl_servo2(angulo2, hat_counters[i])
                    elif servo_selected == 3:
                        # print("Moviendo Servo3")
                        angulo3 = Ctrl_servo3(angulo3, hat_counters[i])
                    elif servo_selected == 4:
                        # print("Moviendo Servo4")
                        angulo4 = Ctrl_servo4(angulo4, hat_counters[i])
                    elif servo_selected == 5:
                        # print("Moviendo Servo5")
                        angulo5 = Ctrl_servo5(angulo5, hat_counters[i])
                    elif servo_selected == 6:
                        # print("Moviendo Servo6")
                        angulo6 = Ctrl_servo6(angulo6, hat_counters[i])

                # Add a small delay to reduce CPU usage
                sleep(0.1)

        except KeyboardInterrupt:
            # Graceful exit
            print("Exiting...")
        finally:
            # Clean up
            pygame.quit()

    #Ver pose de robot
    elif opcion == 9:
        Ver_pose(angulo1, angulo2, angulo3, angulo4, angulo5, angulo6)

    #PARA TESTS
    elif opcion == 12:        
        angulo4 = Ctrl_servo4(angulo4, -30)
        angulo1 = Ctrl_servo1(angulo1, 5)
        angulo2 = Ctrl_servo2(angulo2, -3)
        angulo3 = Ctrl_servo3(angulo3, 10)
        angulo4 = Ctrl_servo4(angulo4, 65)
        angulo6 = Ctrl_servo6(angulo6, -75)

        angulo4 = Ctrl_servo4(angulo4, 0)
        angulo1 = Ctrl_servo1(angulo1, -10)
        angulo2 = Ctrl_servo2(angulo2, 0)
        angulo3 = Ctrl_servo3(angulo3, 10)
        angulo4 = Ctrl_servo4(angulo4, 0)
        angulo6 = Ctrl_servo6(angulo6, 0)

        angulo4 = Ctrl_servo4(angulo4, -30)
        angulo1 = Ctrl_servo1(angulo1, 10)
        angulo2 = Ctrl_servo2(angulo2, -3)
        angulo3 = Ctrl_servo3(angulo3, 10)
        angulo4 = Ctrl_servo4(angulo4, 65)
        angulo6 = Ctrl_servo6(angulo6, -75)

        angulo4 = Ctrl_servo4(angulo4, 0)
        angulo1 = Ctrl_servo1(angulo1, -10)
        angulo2 = Ctrl_servo2(angulo2, 0)
        angulo3 = Ctrl_servo3(angulo3, 10)
        angulo4 = Ctrl_servo4(angulo4, 0)
        angulo6 = Ctrl_servo6(angulo6, 0)

    #Opcion para salir
    elif opcion == 5:
        GPIO.cleanup()
        break

    #Opcion no valida
    else:
        print(Fore.RED + "La opcion seleccionada no existe")