from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.color import Color
import time
from rich.markdown import Markdown
import re
from level.libs.init import init
init()
from galite import enter_is_next  # noqa: E402


input_text_l3lib = [None]

def wow(
    input_txt, 
    start_color=[255, 209, 223],    # 起始颜色（默认樱花粉）
    end_color=[209, 196, 233],      # 结束颜色（默认淡紫）
    text_color="white",              # 文字颜色
    bold=True,                       # 是否加粗
    direction="horizontal",          # 渐变方向: horizontal, vertical
    animate=False,                   # 是否逐字显示动画
    animation_speed=0.1,             # 动画速度（秒）
    wait_input=False,                 # 是否在显示后等待用户输入
    wait=True
):
    """
    打印带渐变背景的彩色文字，可选择是否等待用户输入
    """
    console = Console()
    
    # 检查输入是否为空或无效
    if not input_txt:
        console.print("[red]错误: wow() 收到了空内容[/red]")
        enter_is_next()
        return
    
    # 确保输入是字符串，并检查是否误传了 Panel 对象
    input_txt = str(input_txt)
    if "<rich.panel.Panel object" in input_txt:
        console.print("[red]错误: wow() 收到了 Panel 对象字符串，请直接传递文本内容[/red]")
        enter_is_next()
        return
    
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color
    
    # 创建文本对象
    text = Text(input_txt)
    
    if direction == "vertical":
        # 垂直渐变（按行）
        lines = input_txt.split('\n')
        pos = 0
        for line_idx, line in enumerate(lines):
            if len(lines) > 1:
                ratio = line_idx / (len(lines) - 1)
            else:
                ratio = 0
            r = int(start_r + (end_r - start_r) * ratio)
            g = int(start_g + (end_g - start_g) * ratio)
            b = int(start_b + (end_b - start_b) * ratio)
            
            style = Style(bgcolor=Color.from_rgb(r, g, b), color=text_color, bold=bold)
            for _ in range(len(line)):
                text.stylize(style, pos, pos + 1)
                pos += 1
            pos += 1  # 换行符
    else:
        # 水平渐变（默认，按字符）
        for i in range(len(text.plain)):
            if len(text.plain) > 1:
                ratio = i / (len(text.plain) - 1)
            else:
                ratio = 0
            r = int(start_r + (end_r - start_r) * ratio)
            g = int(start_g + (end_g - start_g) * ratio)
            b = int(start_b + (end_b - start_b) * ratio)
            
            style = Style(bgcolor=Color.from_rgb(r, g, b), color=text_color, bold=bold)
            text.stylize(style, i, i + 1)
    
    # 动画效果
    if animate:
        for i in range(1, len(text.plain) + 1):
            partial = Text(text.plain[:i])
            for span in text._spans:
                if span.start < i:
                    end = min(span.end, i)
                    partial.stylize(span.style, span.start, end)
            console.clear()
            console.print()
            console.print(partial)
            time.sleep(animation_speed)
        console.clear()
        console.print()
        console.print(text)
    else:
        # 无动画，直接打印
        console.print()
        console.print(text)
    
    # 根据参数决定下一步
    if wait_input:
        global input_text_l3lib
        input_text_l3lib[0] = input()
    elif wait:
        enter_is_next()

def markdown(markdown_text: str='# undefined', wait: bool=True):
    console = Console()
    console.clear()
    console.print()
    
    # 检查常见的GFM语法
    gfm_patterns = {
        '任务列表': r'- \[[ x]\]',
        '删除线': r'~~.*~~',
        '警告框(Alerts)': r'>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]'
    }
    
    found = []
    for name, pattern in gfm_patterns.items():
        if re.search(pattern, markdown_text, re.MULTILINE | re.IGNORECASE):
            found.append(name)
    
    if found:
        from rich import print
        print("[yellow]⚠️ 警告: 检测到GFM扩展语法，Rich不支持以下特性:[/yellow]")
        for item in found:
            print(f"  • {item}")
        print("  这些内容将被渲染为普通文本或标准Markdown格式")
        print()
    
    md = Markdown(markdown_text)
    console.print(md)
    if wait:
        enter_is_next()

def hex_to_rgb(hex_color: str) -> list:
    """HEX 转 RGB，返回 [R, G, B]"""
    hex_color = hex_color.replace('#', '')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return [r, g, b]