from MenuLite.MlMain import ml_input
from MenuLite.MlMain import set_condition_var
import shared_data
from level.libs.l3lib import wow
import sys
import os
from pathlib import Path
import build_package
import lica
import wtprogress
import threading
import time
import argparse
import M2G
from rich.traceback import install
from galite import clear

install(show_locals=True)  # 安装 Rich 的 traceback 处理器

build_package

log_dir = None
log_path = None
is_loading = True


def loading():
    while is_loading:
        # 使用缓动函数实现加速再减速
        for t in range(101):
            if not is_loading:
                wtprogress.close()
                return
            progress = t / 100
            eased = progress * progress * (3 - 2 * progress)
            now = 1 + eased * 99

            wtprogress.show(now)
            time.sleep(0.01)

        for t in range(101):
            if not is_loading:
                wtprogress.close()
                return
            progress = t / 100
            eased = 1 - (progress * progress * (3 - 2 * progress))
            now = 1 + eased * 99

            wtprogress.show(now)
            time.sleep(0.01)
    wtprogress.close()


def init_pkg():

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
        lica.unpack(
            os.path.join(base_path, "res.lica"),
            os.path.join(
                os.path.dirname(sys.executable)
                if getattr(sys, "frozen", False)
                else base_path,
                "res",
            ),
        )

    global log_dir, log_path

    if getattr(sys, "frozen", False):
        # 打包成 exe 后
        log_dir = Path(sys.executable).parent
    else:
        # 开发环境
        log_dir = Path(__file__).parent

def parser_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--RNT", dest="dev", action="store_true", help="以Dev身份访问")
    parser.add_argument(
        "--M2G",
        dest="m2g",
        type=str,
        help="启用MarkdownToGalite助理，用法：--M2G '目标文件夹'",
    )
    parser.add_argument("--restart", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.dev:
        wow(
            """
██████╗ ███████╗   ███╗   ██╗ ██████╗ ██╗    ██╗██╗████████╗███████╗██╗  ██╗████████╗
██╔══██╗██╔════╝██╗████╗  ██║██╔═══██╗██║    ██║██║╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝
██████╔╝█████╗  ╚═╝██╔██╗ ██║██║   ██║██║ █╗ ██║██║   ██║   █████╗   ╚███╔╝    ██║   
██╔══██╗██╔══╝  ██╗██║╚██╗██║██║   ██║██║███╗██║╚═╝   ██║   ██╔══╝   ██╔██╗    ██║   
██║  ██║███████╗╚═╝██║ ╚████║╚██████╔╝╚███╔███╔╝██╗   ██║   ███████╗██╔╝ ██╗   ██║   
╚═╝  ╚═╝╚══════╝   ╚═╝  ╚═══╝ ╚═════╝  ╚══╝╚══╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝   
""",
            start_color=[51, 51, 51],
            end_color=[61, 61, 61],
            wait=False,
        )
        wow("终端无限，故事可见", text_color="black", wait=False)
        print("Copyright (c) 2026 Argon")
        print("你正在通过Dev身份访问")
        if args.m2g:
            target_dir = args.m2g
            level_dir = Path("level")
            level_dir.mkdir(exist_ok=True)
            md_files = [
                f
                for f in os.listdir(target_dir)
                if f.endswith(".md") and os.path.isfile(os.path.join(target_dir, f))
            ]
            if not md_files:
                print(f"❌ 在 {target_dir} 中没有找到 .md 文件")
                return

            print(f"📁 找到 {len(md_files)} 个 Markdown 文件")

            # 遍历每个 .md 文件
            for md_file in md_files:
                input_path = os.path.join(target_dir, md_file)
                # 输出到 level 文件夹，文件名不变（扩展名改为 .py）
                output_name = md_file.replace(".md", ".py")
                output_path = level_dir / output_name

                print(f"🔄 转换: {md_file} -> {output_path}")
                M2G.convert_file(input_path, str(output_path))

            print("✅ 所有文件转换完成！")
        sys.exit(0)


def all_init():
    init_pkg()
    clear()
    try:
        with open("now", "r", encoding="utf-8") as f:
            level = f.read().strip()
            if level:
                shared_data.condition_vars = True
                set_condition_var("new_game", True)
    except FileNotFoundError:
        pass


def init():
    wtprogress.close()
    parser_init()
    loading_t = threading.Thread(target=loading)
    loading_t.start()
    all_init()
    global is_loading
    is_loading = False
    ml_input()


if __name__ == "__main__":
    init()
