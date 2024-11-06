from PIL import Image
import glob
import os

def convert_frames_to_webp(input_folder, output_file, duration=100):
    """
    将指定文件夹下的所有PNG图片转换为webp动画
    """
    # 打印当前工作目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f"要查找的文件夹路径: {input_folder}")
    
    # 确认文件夹是否存在
    if not os.path.exists(input_folder):
        print(f"错误：文件夹 '{input_folder}' 不存在！")
        return
        
    # 获取所有PNG图片
    search_pattern = os.path.join(input_folder, "*.png")
    print(f"搜索模式: {search_pattern}")
    
    frame_files = glob.glob(search_pattern)
    
    # 打印文件夹内容
    print(f"\n文件夹 '{input_folder}' 中的所有文件:")
    for file in os.listdir(input_folder):
        print(f"  - {file}")
    
    if not frame_files:
        print("\n未找到PNG图片文件！")
        print("请检查:")
        print("1. 文件扩展名是否为小写的.png")
        print("2. 图片文件是否确实在指定文件夹中")
        return
    
    # 读取第一张图片
    frames = []
    first_frame = Image.open(frame_files[0])
    
    # 读取所有图片
    for frame_file in frame_files:
        frame = Image.open(frame_file)
        frames.append(frame)
    
    print(f"正在处理 {len(frames)} 张图片...")
    
    # 保存为webp动画
    first_frame.save(
        output_file,
        format='webp',
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=0
    )
    
    print(f"动画已保存为: {output_file}")

if __name__ == "__main__":
    # 使用示例
    input_folder = "2_frames"  # 输入文件夹路径
    output_file = "animation.webp"  # 输出文件路径
    duration = 60  # 每帧持续时间（毫秒）
    
    convert_frames_to_webp(input_folder, output_file, duration) 