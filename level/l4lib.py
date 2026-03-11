from rich.console import Console
from rich.text import Text
import numpy as np
from PIL import Image
from galite import enter_is_next
from level.init import init
import os
import sys

init()

chars = []


def resource_path(relative_path):
    """获取资源的绝对路径（兼容开发环境和 PyInstaller 打包后）"""
    try:
        # PyInstaller 打包后的临时目录
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境，使用当前目录
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def image(img_file: str, width: int = 120, char: str = "█"):
    console = Console()
    
    # 使用 resource_path 获取正确的文件路径
    file_path = resource_path(img_file)
    img = Image.open(file_path)

    height = int(img.height / img.width * width * 0.5)
    img_small = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = np.array(img_small)

    def rgb_to_ansi(r, g, b):
        return f"rgb({r},{g},{b})"

    console.clear()
    console.print()

    for y in range(height):
        line = Text()
        for x in range(width):
            r, g, b = pixels[y, x]
            line.append(char, style=rgb_to_ansi(r, g, b))
        console.print(line)
    enter_is_next()