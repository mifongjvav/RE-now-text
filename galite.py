from terminaltables3 import DoubleTable, SingleTable, AsciiTable
import sys
import subprocess
import getpass

# 全局当前主题类（默认双线框）
_current_theme = DoubleTable

# 用户输入存储（列表，保证跨模块可变）
input_text = [None]

def set_theme(theme_name: str = 'double'):
    """设置全局表格主题"""
    global _current_theme
    if theme_name == 'double':
        _current_theme = DoubleTable
    elif theme_name == 'single':
        _current_theme = SingleTable
    elif theme_name == 'ascii':
        _current_theme = AsciiTable
    else:
        raise ValueError("无效的主题，请选择 'double', 'single' 或 'ascii'")

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

def P(title: str = "undefined", text: str = "undefined", theme=None):
    clear()
    table_data = [[text]]
    table_class = _get_table_class(theme)
    table = table_class(table_data)
    table.title = title
    print(f'\n{table.table}')
    enter_is_next()

def S(title: str = "undefined", text: str = "undefined", theme=None):
    clear()
    table_data = [[text]]
    table_class = _get_table_class(theme)
    table = table_class(table_data)
    table.title = title
    print(f'\n{table.table}')
    global input_text
    input_text[0] = input()

def A(name: str = "undefined", level: int = 0, theme=None):
    clear()
    with open('advancements', 'w', encoding='utf-8') as f:
        f.write(f'{name}:{level}')
    table_data = [[name]]
    table_class = _get_table_class(theme)
    table = table_class(table_data)
    if level == 0:
        table.title = '进度已完成！'
        print(f'\n\033[1;37;43m{table.table}\033[0m')
    elif level == 1:
        table.title = '目标已完成！'
        print(f'\n\033[1;37;43m{table.table}\033[0m')
    else:
        table.title = '挑战已完成！'
        print(f'\n\033[1;37;45m{table.table}\033[0m')
    enter_is_next()

def N(path: str):
    clear()
    subprocess.run(["python", path])

def E(code: int):
    clear()
    sys.exit(code)