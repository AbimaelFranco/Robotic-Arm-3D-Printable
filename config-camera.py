"""
This script configures the camera on a Raspberry Pi to detect specified colors in real-time using OpenCV and Picamera2. 
It helps to determine the HSV color ranges based on lighting conditions and establish the camera position through the preview stream.
"""
import cv2
import numpy as np
from picamera2 import Picamera2, Preview

def detect_color_in_video(color_ranges):
    """
    Configure the camera and detect specified colors in real-time video feed.
    
    Parameters:
    color_ranges (dict): Dictionary with color names as keys and tuples of lower and upper HSV ranges as values.
    """
    # Configure the camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()
        
        # Rotate the image 180°
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        for color_name, (lower_color, upper_color) in color_ranges.items():
            # Create a mask with the specified color range
            mask = cv2.inRange(hsv_frame, lower_color, upper_color)
            
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # If contours are found, draw the largest contour
            if contours:
                # Find the contour with the largest area
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Draw the largest contour on the original frame
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                
                # Get the moments of the contour to find the center
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # Draw the color name at the center of the contour
                    cv2.putText(frame, color_name, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Display the original frame
        cv2.imshow("Original Frame", frame)
        
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the windows
    cv2.destroyAllWindows()
    picam2.stop()

if __name__ == "__main__":
    # Specify the color ranges in HSV
    color_ranges = {
        "Red": (np.array([170, 100, 100]), np.array([179, 255, 255])),
        "Yellow": (np.array([20, 50, 50]), np.array([30, 255, 255])),
        "Green": (np.array([50, 50, 50]), np.array([85, 255, 255]))
    }

    detect_color_in_video(color_ranges)
