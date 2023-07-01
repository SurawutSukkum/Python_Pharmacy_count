import cv2
import os
from time import process_time
# Constants for calibration
reference_width_mm = 10  # Width of the reference object in mm
reference_width_pixels = 10  # Width of the reference object in the image in pixels
vid = cv2.VideoCapture(1)       
# Start the stopwatch / counter 
t1_start = process_time()
while True:
    
    #img = cv2.imread(IMAGE_PATH)
    ret, image  = vid.read()
    x = 100
    y = 100
    w = 1000
    h = 800
    
    cropped_image = image[y:y+h, x:x+w]
    #cv2.THRESH_BINARY_INV
    image_contour_thred1 = cropped_image.copy()
    gray = cv2.cvtColor(image_contour_thred1, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    canny = cv2.Canny(blur, 30, 100)
    dilated = cv2.dilate(canny, (1, 1), iterations=0)
    
    cv2.imshow('dilated', dilated)    
    contours1, hierarchy1 = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    min_area_threshold = 1000
    c=0
    for contour in contours1:
     c=c+1
     print(len(contours1))
     area_pixels = cv2.contourArea(contour)
     print(area_pixels)
     # Convert the area from pixels to mm
     area_mm = area_pixels    
     if  (area_pixels > min_area_threshold):
       if  (area_pixels < (min_area_threshold + 50)):         
         image_contour_thred1  = cv2.putText( image_contour_thred1 , "Count: "+str(len(contours1)), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
         #image_contour_thred1  = cv2.putText( image_contour_thred1 , "Area: "+str(area_pixels), (10,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
         cv2.drawContours(image=image_contour_thred1, contours=contours1, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
         cv2.imshow('Pharmacy count: ', image_contour_thred1)

    if (cv2.waitKey(30) == 27):
      break
        
vid.release()
cv2.destroyAllWindows()
