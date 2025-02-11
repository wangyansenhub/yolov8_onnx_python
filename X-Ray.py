import cv2
import numpy as np
import os


def contrast_stretch(image):
    min_val = np.min(image)
    max_val = np.max(image)
    stretched_image = ((image - min_val) * (1.0 / (max_val - min_val))) * 255.0
    return stretched_image.astype(np.uint8)


def calculate_r_value(image_path, output_folder_path):
    image_name = image_path.split("/")[-1]
    image = cv2.imread(image_path, 0)
    height, width = image.shape[:2]
    half_width = width // 2

    low_energy_image = image[:, :half_width]
    high_energy_image = image[:, half_width:]

    # 中值滤波处理
    low_energy_image = cv2.medianBlur(low_energy_image, 5)
    high_energy_image = cv2.medianBlur(high_energy_image, 5)

    # low_energy_image = cv2.GaussianBlur(low_energy_image, (3, 3), 0)
    # high_energy_image = cv2.GaussianBlur(high_energy_image, (3, 3), 0)
    low_energy_image = contrast_stretch(low_energy_image)
    high_energy_image = contrast_stretch(high_energy_image)

    # # 计算直方图
    # hist_low = cv2.calcHist([low_energy_image], [0], None, [256], [0, 256])
    # hist_high = cv2.calcHist([high_energy_image], [0], None, [256], [0, 256])
    # similarity = cv2.compareHist(hist_low, hist_high, cv2.HISTCMP_BHATTACHARYYA)

    # # 使用SIFT特征检测器和描述符
    # sift = cv2.SIFT_create()
    # kp1, des1 = sift.detectAndCompute(low_energy_image, None)
    # kp2, des2 = sift.detectAndCompute(high_energy_image, None)

    # # 使用BFMatcher进行特征匹配
    # bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    # matches = bf.knnMatch(des1, des2, k=2)

    # good = []
    # for m, n in matches:
    #     if m.distance < 0.75 * n.distance:
    #         good.append(m)

    # match_count = len(good)
    # if match_count < 10:
    #     good = []
    #     for m, n in matches:
    #         if m.distance < 0.85 * n.distance:
    #             good.append(m)

    # if len(good) < 4:
    #     # 若基于当前特征匹配不足，利用直方图相似性处理
    #     if similarity < 0.5:
    #         # 可以尝试特殊处理，例如再次调整滤波参数、重新提取特征
    #         low_energy_image = cv2.GaussianBlur(low_energy_image, (3, 3), 0)
    #         high_energy_image = cv2.GaussianBlur(high_energy_image, (3, 3), 0)
    #         sift = cv2.SIFT_create()
    #         kp1, des1 = sift.detectAndCompute(low_energy_image, None)
    #         kp2, des2 = sift.detectAndCompute(high_energy_image, None)
    #         bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    #         matches = bf.knnMatch(des1, des2, k=2)
    #         good = []
    #         for m, n in matches:
    #             if m.distance < 0.8 * n.distance:
    #                 good.append(m)

    # if len(good) < 4:
    #     raise ValueError("Not enough good matches to calculate homography.")

    # src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    # dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # 计算变换矩阵
    # M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

    M = np.array([[9.98505781e-01, 5.73400445e-04, 1.66157137e+00],
                  [1.35996587e-03, 1.00206315e+00, 1.62500326e-01],
                  [2.84320693e-06, 1.27379662e-06, 1.00000000e+00]])


    # 对高能图像进行变换
    high_energy_image_warped = cv2.warpPerspective(high_energy_image, M, (half_width, height))

    epsilon = 0.00001
    r_value_image = (high_energy_image_warped.astype(np.float32) + epsilon) / (low_energy_image.astype(np.float32) + epsilon)

    r_value_image = np.stack((low_energy_image, high_energy_image_warped, r_value_image), axis=-1)
    r_value_image_display = (r_value_image * 255).astype(np.uint8)

    cv2.imwrite(output_folder_path + '/' + image_name, r_value_image_display)


input_folder_path = "data/yin"
output_folder_path = "data/yin-result-1-140"
os.makedirs(output_folder_path, exist_ok=True)
tif_files = [f for f in os.listdir(input_folder_path) if f.endswith('.tif')]
tif_files.sort()
for i in range(0, len(tif_files)):
    image_path = os.path.join(input_folder_path, tif_files[i])
    calculate_r_value(image_path, output_folder_path)
