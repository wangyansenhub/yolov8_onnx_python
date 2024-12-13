import cv2
import numpy as np, glob

image_path = r'D:\result_G140\*.tif'
for i in glob.glob(image_path):
    image = cv2.imread(i)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    threshold_value = 127  
    max_value = 255
    ret, thresh = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_contour_area = 100  # 面积阈值

    # 筛选轮廓
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    drawing = np.zeros_like(image)
    cv2.drawContours(drawing, filtered_contours, -1, (0, 255, 0), 2)

    output_file_path = 'D:\gitlab\yolov8\info.txt'
    with open(output_file_path, 'w') as f:

        for i, cnt in enumerate(filtered_contours):
            x, y, w, h = cv2.boundingRect(cnt)
            
            center_x = x + w // 2
            center_y = y + h // 2
            
            f.write(f"{i}: ({center_x}, {center_y}), {w}, {h}\n")
            cv2.rectangle(drawing, (x, y), (x + w, y + h), (255, 255, 0), 2)

    cv2.imshow('Filtered Contours', drawing)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
