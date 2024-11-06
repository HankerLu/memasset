import os
from PIL import Image
import glob

def create_sprite_sheet(input_folder, output_path, images_per_row=8):
    # 获取所有PNG文件并按名称排序
    png_files = sorted(glob.glob(os.path.join(input_folder, "*.png")))
    
    if not png_files:
        print(f"在 {input_folder} 中没有找到PNG文件")
        return
    
    # 打开第一张图片获取尺寸
    first_image = Image.open(png_files[0])
    img_width, img_height = first_image.size
    
    # 计算sprite sheet的尺寸
    num_images = len(png_files)
    num_rows = (num_images + images_per_row - 1) // images_per_row
    sheet_width = img_width * min(images_per_row, num_images)
    sheet_height = img_height * num_rows
    
    # 创建新的空白图片
    sprite_sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
    
    # 按顺序粘贴图片
    for idx, png_file in enumerate(png_files):
        img = Image.open(png_file)
        row = idx // images_per_row
        col = idx % images_per_row
        x = col * img_width
        y = row * img_height
        sprite_sheet.paste(img, (x, y))
    
    # 保存sprite sheet
    sprite_sheet.save(output_path, 'PNG')
    print(f"Sprite sheet已保存到: {output_path}")

def process_all_2frames_folders(root_directory):
    # 查找所有2_frames文件夹
    for dirpath, dirnames, filenames in os.walk(root_directory):
        if os.path.basename(dirpath) == "2_frames":
            print(f"处理文件夹: {dirpath}")
            # 创建输出文件夹（如果不存在）
            output_dir = os.path.join(os.path.dirname(dirpath), "sprite_sheets")
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成输出文件名
            folder_name = os.path.basename(os.path.dirname(dirpath))
            output_path = os.path.join(output_dir, f"{folder_name}_sprite_sheet.png")
            
            # 创建sprite sheet
            create_sprite_sheet(dirpath, output_path)

if __name__ == "__main__":
    # 指定要搜索的根目录
    root_dir = "."  # 当前目录，可以修改为其他路径
    process_all_2frames_folders(root_dir) 