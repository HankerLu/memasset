import cv2
import numpy as np
import os
from PIL import Image
import glob

def extract_robot(image_path, output_path):
    # 读取图片
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # 转换为RGBA格式（如果不是的话）
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 转换为HSV颜色空间以更好地处理颜色
    hsv = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2HSV)
    
    # 创建掩码来检测背景
    # 注意：这里的阈值可能需要根据实际图片调整
    lower_bound = np.array([0, 0, 200])  # 接近白色的背景
    upper_bound = np.array([180, 30, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # 反转掩码来获取机器人区域
    mask = cv2.bitwise_not(mask)
    
    # 使用形态学操作来改善掩码
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 创建透明背景的输出图像
    output = img.copy()
    output[mask == 0] = [0, 0, 0, 0]  # 设置背景为透明
    
    # 保存结果
    cv2.imwrite(output_path, output)

def process_all_2frames_folders(root_directory):
    # 查找所有2_frames文件夹
    for dirpath, dirnames, filenames in os.walk(root_directory):
        if os.path.basename(dirpath) == "2_frames":
            print(f"处理文件夹: {dirpath}")
            
            # 创建输出文件夹
            output_dir = os.path.join(os.path.dirname(dirpath), "extracted_robots")
            os.makedirs(output_dir, exist_ok=True)
            
            # 处理文件夹中的所有PNG文件
            png_files = glob.glob(os.path.join(dirpath, "*.png"))
            for png_file in png_files:
                # 生成输出文件路径
                filename = os.path.basename(png_file)
                output_path = os.path.join(output_dir, f"extracted_{filename}")
                
                print(f"正在处理: {filename}")
                extract_robot(png_file, output_path)

if __name__ == "__main__":
    root_dir = "."  # 当前目录，可以修改为其他路径
    process_all_2frames_folders(root_dir) 