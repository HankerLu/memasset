from PIL import Image
import os
import argparse

def resize_frame(frame, target_width=660, target_height=793):
    """
    调整帧的大小，保持比例并填充透明背景
    """
    # 计算缩放比例
    original_width, original_height = frame.size
    width_ratio = target_width / original_width
    height_ratio = target_height / original_height
    scale_ratio = min(width_ratio, height_ratio)
    
    # 计算缩放后的尺寸
    new_width = int(original_width * scale_ratio)
    new_height = int(original_height * scale_ratio)
    
    # 调整帧的大小
    resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 创建新的透明背景图像
    new_frame = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
    
    # 计算粘贴位置（居中）
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    
    # 将调整后的帧粘贴到新图像上
    new_frame.paste(resized_frame, (paste_x, paste_y))
    
    return new_frame

def gif_to_spritesheet(gif_path, output_folder='sprite_sheets'):
    """
    将GIF文件转换为sprite sheet
    
    Args:
        gif_path (str): GIF文件的路径
        output_folder (str): 输出文件夹路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 打开GIF文件
    gif = Image.open(gif_path)
    
    # 获取GIF的所有帧并调整大小
    frames = []
    try:
        while True:
            # 复制当前帧并调整大小
            frame = gif.copy()
            resized_frame = resize_frame(frame)
            frames.append(resized_frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    # 设置固定的帧尺寸
    frame_width = 660
    frame_height = 793
    frame_count = len(frames)
    
    # 计算sprite sheet的尺寸
    frames_per_row = 8
    rows = (frame_count + frames_per_row - 1) // frames_per_row
    
    # 创建新的图像用于sprite sheet
    spritesheet_width = frame_width * min(frames_per_row, len(frames))
    spritesheet_height = frame_height * rows
    spritesheet = Image.new('RGBA', (spritesheet_width, spritesheet_height), (0, 0, 0, 0))
    
    # 将所有帧放置到sprite sheet中
    for idx, frame in enumerate(frames):
        row = idx // frames_per_row
        col = idx % frames_per_row
        x = col * frame_width
        y = row * frame_height
        spritesheet.paste(frame, (x, y))
    
    # 修改输出文件名格式
    gif_name = os.path.splitext(os.path.basename(gif_path))[0]
    output_filename = f"{gif_name}_{frame_count}f_{frame_width}x{frame_height}_spritesheet.png"
    output_path = os.path.join(output_folder, output_filename)
    
    # 保存sprite sheet
    spritesheet.save(output_path, 'PNG')
    print(f"Sprite sheet已保存到: {output_path}")
    print(f"帧数: {frame_count}, 单帧分辨率: {frame_width}x{frame_height}")

def main():
    parser = argparse.ArgumentParser(description='将GIF转换为sprite sheet')
    parser.add_argument('gif_path', help='GIF文件的路径')
    parser.add_argument('-o', '--output', default='sprite_sheets',
                      help='输出文件夹路径 (默认: sprite_sheets)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.gif_path):
        print(f"错误: 文件 '{args.gif_path}' 不存在")
        return
    
    gif_to_spritesheet(args.gif_path, args.output)

if __name__ == "__main__":
    main() 