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
    """获取资源的绝对路径"""
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = ""

    return os.path.join(base_path, relative_path)


def image(img_file: str, width: int = 120, char: str = "█", square: bool = False):
    console = Console()
    file_path = resource_path(img_file)
    img = Image.open(file_path)

    if square:
        # 每个像素用两个字符，像素宽度 = 总字符宽度 // 2
        pix_width = width // 2
        if pix_width == 0:
            pix_width = 1  # 确保至少一列
        # 高度计算：由于两个字符的宽度约等于一个字符的高度，无需额外补偿
        pix_height = int(img.height / img.width * pix_width)
    else:
        # 原始模式：一个像素一个字符，补偿字符宽高比（0.5 因子）
        pix_width = width
        pix_height = int(img.height / img.width * width * 0.5)

    # 确保高度至少为1
    if pix_height < 1:
        pix_height = 1

    img_small = img.resize((pix_width, pix_height), Image.Resampling.LANCZOS)
    pixels = np.array(img_small)

    def rgb_to_ansi(r, g, b):
        return f"rgb({r},{g},{b})"

    console.clear()
    console.print()

    for y in range(pix_height):
        line = Text()
        for x in range(pix_width):
            r, g, b = pixels[y, x][:3]
            colored_char = Text(char, style=rgb_to_ansi(r, g, b))
            if square:
                # 同一个像素用两个相同颜色的字符并排
                line.append(colored_char)
                line.append(colored_char)
            else:
                line.append(colored_char)
        console.print(line)

    enter_is_next()
