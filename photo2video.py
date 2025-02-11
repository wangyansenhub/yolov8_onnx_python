import cv2
import os

image_folder = 'file_path'
video_name = 'output_video.mp4'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
images.sort()

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

fps = 3
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

for image in images:
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    video.write(frame)

video.release()

print(f"视频已生成：{video_name}")
