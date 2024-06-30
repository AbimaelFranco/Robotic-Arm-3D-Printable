import cv2
import numpy as np
from picamera2 import Picamera2, Preview
import time

def detect_color_in_photo(color_ranges):
    try:
        # Configurar la cámara
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"format": "XRGB8888", "size": (640, 480)})
        picam2.configure(config)
        picam2.start()
        
        # Esperar un momento para que la cámara se estabilice
        time.sleep(2)
        
        # Capturar una foto
        frame = picam2.capture_array()
        
        # Girar la imagen 180°
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        
        # Convertir el frame a espacio de color HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Contadores de píxeles para cada color
        color_counts = {color: 0 for color in color_ranges}
        
        for color_name, (lower_color, upper_color) in color_ranges.items():
            # Crear una máscara con el rango de colores especificado
            mask = cv2.inRange(hsv_frame, lower_color, upper_color)
            
            # Contar los píxeles de la máscara
            color_counts[color_name] = cv2.countNonZero(mask)
            
        # Determinar el color predominante
        predominant_color = max(color_counts, key=color_counts.get)
        if color_counts[predominant_color] == 0:
            result = "No se ha detectado ningún color especificado"
        else:
            result = f"El color predominante es: {predominant_color}"
        
        # Cerrar la cámara
        picam2.stop()
        picam2.close()
        
        return result, predominant_color

    except Exception as e:
        return f"Error al intentar capturar la imagen: {str(e)}"