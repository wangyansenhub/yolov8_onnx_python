import cv2
import os

def extract_frames(video_path, output_folder, interval=3):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        raise FileNotFoundError("视频文件不存在")

    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        raise IOError("无法打开视频文件")
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print(total_frames, fps)
    count = 0
    frame_count = 0
    
    while True:
        success, image = vidcap.read()
        if not success:
            break
        
        if count % interval == 0:
            output_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(output_path, image)
            # print(f"Frame {count} saved as {output_path}")
            frame_count += 1
        
        count += 1
    print("视频帧提取完成")
    
    vidcap.release()

# 使用函数
video_path = r"./traffic.mp4"  # 修改为单个反斜杠或正斜杠
output_folder = r'./sample'
extract_frames(video_path, output_folder, interval=10)
