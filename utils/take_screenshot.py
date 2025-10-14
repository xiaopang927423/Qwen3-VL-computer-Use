import pyscreenshot as ImageGrab
import time
import os
from datetime import datetime
from PIL import Image


def take_screenshot(save_path=None, target_width=1728, target_height=1117):
    """
    截取屏幕截图，并根据目标分辨率调整尺寸

    Args:
        save_path (str, optional): 保存路径，默认为 src/screenshots/screenshot_YYYYMMDD_HHMMSS.png
        target_width (int): 目标宽度，默认为1728
        target_height (int): 目标高度，默认为1117

    Returns:
        str: 保存的截图路径
    """
    # 等待几秒钟，确保你有时间切换到需要截屏的窗口
    print("即将截图，3秒后执行...请切换到需要截图的界面")
    time.sleep(3)

    # 创建截图目录（如果不存在）
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # 生成带时间戳的文件名
    if save_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")

    # 截取整个屏幕
    screenshot = ImageGrab.grab()

    # 获取原始屏幕分辨率
    original_width, original_height = screenshot.size
    print(f"原始屏幕分辨率: {original_width}x{original_height}")

    # 调整图像大小以匹配目标分辨率
    # 这解决了Retina显示屏截图尺寸是实际显示尺寸两倍的问题
    if original_width != target_width or original_height != target_height:
        print(f"调整图像尺寸从 {original_width}x{original_height} 到 {target_width}x{target_height}")
        screenshot = screenshot.resize((target_width, target_height), Image.LANCZOS)
        print(f"图像尺寸已调整为: {target_width}x{target_height}")

    # 保存截图
    screenshot.save(save_path, "PNG", optimize=True)
    print(f"截图已保存到: {save_path}")

    return save_path
