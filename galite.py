from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print
import sys
import subprocess
import getpass
import importlib
import traceback
import builtins
from rich.align import Align
from rich.live import Live
import time
from rich.traceback import install
from io import StringIO
import threading

install(show_locals=True)  # 安装 Rich 的 traceback 处理器

width = 20

# 创建全局 Rich 控制台
console = Console()

# 全局当前主题
_current_theme = "rounded"

# 用户输入存储
input_text = [None]
return_value = [None]


def set_theme(theme_name: str = "rounded"):
    """设置全局表格主题"""
    global _current_theme
    valid_themes = ["double", "single", "ascii", "rounded"]
    if theme_name in valid_themes:
        _current_theme = theme_name
    else:
        raise ValueError(f"无效的主题，请选择: {', '.join(valid_themes)}")


def _render_with_theme(title, content, theme=None):
    """根据主题渲染内容，返回 Panel 对象（圆角）或字符串（其他）"""
    use_theme = theme if theme is not None else _current_theme

    if use_theme == "rounded":
        # 创建表格
        table = Table(
            show_header=False,
            box=None,
            pad_edge=False,
            expand=False,
            collapse_padding=True,
            highlight=True,
            show_footer=False,
            show_edge=False,
        )
        table.add_column("content", style="white", no_wrap=False, overflow="fold")
        # 处理不同类型的内容
        if isinstance(content, list):
            for row in content:
                if isinstance(row, list):
                    # 直接添加整个列表作为一行，Rich 会自动展开
                    table.add_row(*[str(item) for item in row])
                else:
                    table.add_row(str(row))
        else:
            table.add_row(str(content))

        panel = Panel(
            table,
            title=title,
            border_style="white",
            padding=(1, 2),
        )
        return panel
    else:
        from terminaltables3 import DoubleTable, SingleTable, AsciiTable

        if use_theme == "double":
            table_class = DoubleTable
        elif use_theme == "single":
            table_class = SingleTable
        else:
            table_class = AsciiTable

        if isinstance(content, str):
            table_data = [[content]]
        elif isinstance(content, list) and content and isinstance(content[0], list):
            table_data = content
        elif isinstance(content, list):
            table_data = [content]
        else:
            table_data = [[str(content)]]

        table = table_class(table_data)
        table.title = title

        return table.table


def clear():
    """清屏"""
    if sys.platform == "win32":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)


def enter_is_next():
    print("按回车键继续...", end="", flush=True)
    getpass.getpass("")
    time.sleep(0.2)


def table_to_string(table):
    """将 Rich Table 转换为字符串"""
    console = Console(file=StringIO(), force_terminal=False)
    console.print(table)
    return console.file.getvalue()


def P(
    title: str = "undefined",
    text: str = "undefined",
    theme=None,
    hide: bool = False,
    animate: bool = True,
    animate_speed: float = 0.05,
):
    """显示对话框，支持文字逐字动画，按任意键跳过"""
    global input_text, return_value

    clear()

    if not hide:
        console.print()

        if animate:
            # 直接用 Live 从空开始，但第一帧就显示第一个字符
            stop_animation = threading.Event()

            def check_keypress():
                if sys.platform == "win32":
                    import msvcrt

                    msvcrt.getch()
                else:
                    import select

                    select.select([sys.stdin], [], [], None)
                    sys.stdin.read(1)
                stop_animation.set()

            key_thread = threading.Thread(target=check_keypress, daemon=True)
            key_thread.start()

            # 创建初始 Panel（空内容，但不打印）
            empty_rendered = _render_with_theme(title, "", theme)
            aligned_panel = Align.left(empty_rendered)

            with Live(
                aligned_panel, console=console, refresh_per_second=20, transient=False
            ) as live:
                current_text = ""
                for char in text:
                    if stop_animation.is_set():
                        current_text = text
                        new_rendered = _render_with_theme(title, current_text, theme)
                        live.update(Align.left(new_rendered))
                        break

                    current_text += char
                    new_rendered = _render_with_theme(title, current_text, theme)
                    live.update(Align.left(new_rendered))
                    time.sleep(animate_speed)

        else:
            # 非动画分支
            rendered = _render_with_theme(title, text, theme)
            if isinstance(rendered, str):
                console.print(rendered)
            else:
                console.print(Align.left(rendered))

        enter_is_next()

    rendered = _render_with_theme(title, text, theme)
    if hasattr(rendered, "__rich_console__"):
        return_value[0] = table_to_string(rendered)
    else:
        return_value[0] = str(rendered)


def main_menu_p(title: str = "undefined", text=None, theme=None):
    rendered = _render_with_theme(title, text, theme)
    console.print()
    if isinstance(rendered, str):
        console.print(rendered)  # 字符串直接打印
    else:
        console.print(Align.left(rendered))  # Rich 对象居左


def S(
    title: str = "undefined",
    text: str = "undefined",
    theme=None,
    hide: bool = False,
    animate: bool = True,
    animate_speed: float = 0.05,
):
    """输入框，支持逐字动画，按任意键跳过"""
    global input_text, return_value

    clear()

    if not hide:
        console.print()

        if animate:
            empty_rendered = _render_with_theme(title, " ", theme)  # 用一个空格占位

            if isinstance(empty_rendered, str):
                console.print(empty_rendered)
                input_text[0] = input()
                return_value[0] = empty_rendered
                return

            aligned_panel = Align.left(empty_rendered)

            stop_animation = threading.Event()

            def check_keypress():
                if sys.platform == "win32":
                    import msvcrt

                    msvcrt.getch()
                else:
                    import select

                    select.select([sys.stdin], [], [], None)
                    sys.stdin.read(1)
                stop_animation.set()

            key_thread = threading.Thread(target=check_keypress, daemon=True)
            key_thread.start()

            with Live(
                aligned_panel, console=console, refresh_per_second=20, transient=False
            ) as live:
                current_text = ""
                for char in text:
                    if stop_animation.is_set():
                        current_text = text
                        new_rendered = _render_with_theme(title, current_text, theme)
                        live.update(Align.left(new_rendered))
                        break

                    current_text += char
                    new_rendered = _render_with_theme(title, current_text, theme)
                    live.update(Align.left(new_rendered))
                    time.sleep(animate_speed)

            # 动画结束后，等待用户输入
            input_text[0] = input()
        else:
            rendered = _render_with_theme(title, text, theme)
            if isinstance(rendered, str):
                console.print(rendered)
            else:
                console.print(Align.left(rendered))
            input_text[0] = input()

    rendered = _render_with_theme(title, text, theme)
    if hasattr(rendered, "__rich_console__"):
        return_value[0] = table_to_string(rendered)
    else:
        return_value[0] = str(rendered)


def A(name: str = "undefined", level: int = 0, theme=None):
    clear()

    existing_level = None
    target_line = f"{name}:{level}\n"

    # 检查是否已存在该成就
    try:
        with open("advancements", "r", encoding="utf-8") as f:
            for line in f:
                if line == target_line:
                    existing_level = level
                    break
    except FileNotFoundError:
        pass

    if existing_level is not None:
        level_to_use = existing_level
        title_suffix = "（已存在）"
    else:
        level_to_use = level
        title_suffix = ""
        with open("advancements", "a", encoding="utf-8") as f:
            f.write(target_line)

    # 根据 level 确定标题文字
    if level_to_use == 0:
        title_text = f"进度已完成！{title_suffix}"
    elif level_to_use == 1:
        title_text = f"目标已完成！{title_suffix}"
    else:
        title_text = f"挑战已完成！{title_suffix}"

    # 用 Rich Panel 实现带颜色的成就显示
    if theme == "rounded" or (theme is None and _current_theme == "rounded"):
        # 圆角主题用 Rich
        panel = Panel(
            f"[bold]{name}[/bold]",
            title=title_text,
            border_style="bright_yellow" if level <= 1 else "bright_magenta",
            style="white",
            padding=(1, 2),
        )
        console.print()
        console.print(Align.left(panel))
    else:
        # 其他主题保持原来的 ANSI 颜色逻辑
        if level_to_use <= 1:
            color_code = "\033[1;37;43m"  # 黄底
        else:
            color_code = "\033[1;37;45m"  # 紫底

        table_data = [[name]]
        from terminaltables3 import DoubleTable

        table = DoubleTable(table_data)
        table.title = title_text
        # 非圆角主题用 builtins.print 输出字符串
        builtins.print(f"\n{color_code}{table.table}\033[0m")

    global return_value
    return_value[0] = name
    enter_is_next()  # 确保这个函数里没有 print(panel)


def N(path: str):
    clear()
    try:
        with open("now", "w", encoding="utf-8") as f:
            f.write(path)
        importlib.import_module(path)
    except Exception as e:
        print(f"加载关卡失败: {e}")
        traceback.print_exc()
        enter_is_next()


def E(code: int = 0):
    clear()
    sys.exit(code)


if __name__ == "__main__":
    from i18n import init_lang
    init_lang()
    P("Argon", sys.lang.error.start.galite)
