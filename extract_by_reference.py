import cv2
import numpy as np
import os
from pathlib import Path

def extract_reference_contour(standard_image_path):
    """读取标准图片并获取其轮廓"""
    # 读取标准图片
    img = cv2.imread(str(standard_image_path), cv2.IMREAD_UNCHANGED)
    
    # 转换为灰度图
    if img.shape[-1] == 4:  # 如果是RGBA图片
        # 分离通道
        b, g, r, a = cv2.split(img)
        # 使用alpha通道作为mask
        gray = a
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 调整二值化阈值
    _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    
    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 获取最大轮廓（假设主要物体是最大的轮廓）
    main_contour = max(contours, key=cv2.contourArea)
    
    return main_contour

def process_images(folder_path, standard_image_name, output_folder):
    """处理文件夹中的所有图片"""
    folder_path = Path(folder_path)
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    
    # 获取标准图片的轮廓
    standard_path = folder_path / standard_image_name
    reference_contour = extract_reference_contour(standard_path)
    
    # 获取轮廓的边界框
    x, y, w, h = cv2.boundingRect(reference_contour)
    
    # 处理文件夹中的所有PNG图片
    for image_path in folder_path.glob('*.png'):
        # 跳过标准图片
        if image_path.name == standard_image_name:
            continue
            
        # 读取图片
        img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        
        # 确保图像有alpha通道
        if img.shape[-1] != 4:
            # 如果没有alpha通道，添加一个
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        
        # 提取相同位置的区域
        extracted = img[y:y+h, x:x+w]
        
        # 创建轮廓遮罩
        mask = np.zeros((h, w), dtype=np.uint8)
        adjusted_contour = reference_contour - [x, y]
        cv2.drawContours(mask, [adjusted_contour], -1, 255, -1)
        
        # 创建输出图像（带透明通道）
        result = np.zeros((h, w, 4), dtype=np.uint8)
        
        # 复制RGB通道
        result[..., :3] = extracted[..., :3]
        
        # 设置alpha通道（使用轮廓遮罩）
        result[..., 3] = mask
        
        # 保存结果
        output_path = output_folder / f"extracted_{image_path.name}"
        cv2.imwrite(str(output_path), result)

if __name__ == "__main__":
    # 设置路径
    folder_path = "2_frames"
    standard_image = "standard.jpg"  # 如果标准图片是PNG格式，改为.png
    output_folder = "extracted_frames"
    
    # 处理图片
    process_images(folder_path, standard_image, output_folder)
    print("处理完成！提取的图片已保存到", output_folder) 