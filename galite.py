from terminaltables3 import DoubleTable, SingleTable, AsciiTable
import sys
import subprocess
import getpass
import importlib
import traceback
from rich import print
import builtins

# 全局当前主题类（默认双线框）
_current_theme = DoubleTable

# 用户输入存储（列表，保证跨模块可变）
input_text = [None]
return_value = [None]

# 自定义圆角边框表格类
class RoundedTable(DoubleTable):
    """支持圆角边框的表格"""
    
    # 圆角边框字符
    CHAR_CORNER_TOP_LEFT = '╭'
    CHAR_CORNER_TOP_RIGHT = '╮'
    CHAR_CORNER_BOTTOM_LEFT = '╰'
    CHAR_CORNER_BOTTOM_RIGHT = '╯'
    CHAR_HORIZONTAL = '─'
    CHAR_VERTICAL = '│'
    CHAR_INTERSECTION = '┼'
    CHAR_TOP_INTERSECTION = '┬'
    CHAR_BOTTOM_INTERSECTION = '┴'
    CHAR_LEFT_INTERSECTION = '├'
    CHAR_RIGHT_INTERSECTION = '┤'
    
    @property
    def table(self):
        """重写 table 属性以使用圆角边框"""
        original = super().table
        lines = original.split('\n')
        
        if not lines:
            return original
        
        result = []
        for i, line in enumerate(lines):
            if i == 0:  # 第一行（上边框）
                # 处理标题行
                if line.startswith('╔'):
                    # 找到第一个和最后一个非边框字符的位置
                    chars = list(line)
                    # 左边框
                    chars[0] = self.CHAR_CORNER_TOP_LEFT
                    # 右边框
                    chars[-1] = self.CHAR_CORNER_TOP_RIGHT
                    # 中间的水平线
                    for j in range(1, len(chars)-1):
                        if chars[j] == '═':
                            chars[j] = self.CHAR_HORIZONTAL
                    line = ''.join(chars)
                    
            elif i == len(lines) - 1:  # 最后一行（下边框）
                if line.startswith('╚'):
                    chars = list(line)
                    chars[0] = self.CHAR_CORNER_BOTTOM_LEFT
                    chars[-1] = self.CHAR_CORNER_BOTTOM_RIGHT
                    for j in range(1, len(chars)-1):
                        if chars[j] == '═':
                            chars[j] = self.CHAR_HORIZONTAL
                    line = ''.join(chars)
                    
            else:  # 中间的行
                # 处理分隔线（如果有）
                if line and line[0] in ('╠', '├', '╟'):
                    chars = list(line)
                    chars[0] = self.CHAR_LEFT_INTERSECTION
                    chars[-1] = self.CHAR_RIGHT_INTERSECTION
                    for j in range(1, len(chars)-1):
                        if chars[j] in ('═', '─', '╤', '╪'):
                            chars[j] = self.CHAR_HORIZONTAL
                        elif chars[j] in ('╥', '┬'):
                            chars[j] = self.CHAR_TOP_INTERSECTION
                        elif chars[j] in ('╨', '┴'):
                            chars[j] = self.CHAR_BOTTOM_INTERSECTION
                        elif chars[j] in ('╫', '┼'):
                            chars[j] = self.CHAR_INTERSECTION
                    line = ''.join(chars)
                else:
                    # 普通内容行
                    chars = list(line)
                    if chars and chars[0] == '║':
                        chars[0] = self.CHAR_VERTICAL
                    if chars and chars[-1] == '║':
                        chars[-1] = self.CHAR_VERTICAL
                    line = ''.join(chars)
            
            result.append(line)
        
        return '\n'.join(result)

# 主题映射
THEMES = {
    'double': DoubleTable,
    'single': SingleTable,
    'ascii': AsciiTable,
    'rounded': RoundedTable
}

def set_theme(theme_name: str = 'double'):
    """设置全局表格主题"""
    global _current_theme
    if theme_name in THEMES:
        _current_theme = THEMES[theme_name]
    else:
        raise ValueError(f"无效的主题，请选择: {', '.join(THEMES.keys())}")

def _get_table_class(theme=None):
    """
    根据 theme 参数返回对应的表格类。
    - 如果 theme 是 None，返回全局主题类 _current_theme
    - 如果 theme 是字符串，返回对应的类
    - 如果 theme 已经是类，直接返回
    """
    if theme is None:
        return _current_theme
    if isinstance(theme, str):
        if theme == 'double':
            return DoubleTable
        elif theme == 'single':
            return SingleTable
        elif theme == 'ascii':
            return AsciiTable
        else:
            raise ValueError("无效的主题名，请选择 'double', 'single' 或 'ascii'")
    # 如果 theme 本身就是类（如 DoubleTable），直接返回
    return theme

def clear():
    """清屏"""
    if sys.platform == 'win32':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

def enter_is_next():
    print("按回车键继续...", end='', flush=True)
    getpass.getpass("")

def P(title: str = "undefined", text: str = "undefined", theme=None, hide: bool=False):
    clear()
    table_data = [[text]]
    table_class = _get_table_class(theme)
    table = table_class(table_data)
    table.title = title
    if not hide:
        print(f'\n{table.table}')
        enter_is_next()
    global return_value
    return_value[0] = table.table

def S(title: str = "undefined", text: str = "undefined", theme=None, hide: bool=False):
    clear()
    table_data = [[text]]
    table_class = _get_table_class(theme)
    table = table_class(table_data)
    table.title = title
    if not hide:
        print(f'\n{table.table}')
        global input_text
        input_text[0] = input()
    global return_value
    return_value[0] = table.table

def A(name: str = "undefined", level: int = 0, theme=None):
    clear()
    
    existing_level = None
    target_line = f'{name}:{level}\n'  # 要查找的精确行
    
    # 检查是否已存在该成就（名称和等级都匹配）
    try:
        with open('advancements', 'r', encoding='utf-8') as f:
            for line in f:
                if line == target_line:  # 精确匹配整行
                    existing_level = level  # 既然匹配了，level 就是传入的 level
                    break
    except FileNotFoundError:
        pass
    
    if existing_level is not None:
        # 成就已存在（完全匹配）
        level_to_use = existing_level
        title_suffix = '（已存在）'
    else:
        # 新成就：使用传入的 level，并追加到文件
        level_to_use = level
        title_suffix = ''
        with open('advancements', 'a', encoding='utf-8') as f:
            f.write(target_line)  # 写入完整的一行
    
    # 根据 level_to_use 确定标题文字和颜色
    if level_to_use == 0:
        title_text = f'进度已完成！{title_suffix}'
        color_code = '\033[1;37;43m'  # 黄底
    elif level_to_use == 1:
        title_text = f'目标已完成！{title_suffix}'
        color_code = '\033[1;37;43m'  # 黄底
    else:  # level 2 或其他情况
        title_text = f'挑战已完成！{title_suffix}'
        color_code = '\033[1;37;45m'  # 紫底
    
    # 构建表格并设置标题
    table_data = [[name]]
    table_class = _get_table_class(theme)
    table = table_class(table_data)
    table.title = title_text
    
    # 输出带颜色的表格
    builtins.print(f'\n{color_code}{table.table}\033[0m')
    global return_value
    return_value[0] = table.table
    enter_is_next()

def N(path: str):
    clear()
    try:
        with open('now', 'w', encoding='utf-8') as f:
            f.write(path)
        importlib.import_module(f"level.{path}")
    except Exception as e:
        print(f"加载关卡失败: {e}")
        traceback.print_exc()  # 打印详细堆栈
        enter_is_next()

def E(code: int):
    clear()
    sys.exit(code)

if __name__ == "__main__":
    P('Argon','你应该去启动关卡文件，而不是引擎文件')