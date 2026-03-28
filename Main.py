from MenuLite.MlMain import ml_input
from MenuLite.MlMain import set_condition_var
import shared_data
from level.l3lib import wow
import logging
import coloredlogs
import sys
import os
from pathlib import Path
import build_package
import lica
import wtprogress
import threading
import time
from rich.traceback import install
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

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        lica.unpack(
        os.path.join(base_path, "res.lica"),
        os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else base_path, "res")
    )

    global log_dir, log_path

    if getattr(sys, 'frozen', False):
        # 打包成 exe 后
        log_dir = Path(sys.executable).parent
    else:
        # 开发环境
        log_dir = Path(__file__).parent

def init_log():
    # 创建日志文件路径（指定文件名）
    log_path = log_dir / "debug.log"
    # 清理现有的日志处理器
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)
        
    # 删除旧的日志文件（如果存在）
    try:
        log_path.unlink(missing_ok=True)
    except PermissionError:
        pass

    # 配置文件日志和控制台日志
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    coloredlogs.install(
        level='WARNING', 
        fmt="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
    )

def all_init():
    init_pkg()
    init_log()
    wow("""
██████╗ ███████╗   ███╗   ██╗ ██████╗ ██╗    ██╗██╗████████╗███████╗██╗  ██╗████████╗
██╔══██╗██╔════╝██╗████╗  ██║██╔═══██╗██║    ██║██║╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝
██████╔╝█████╗  ╚═╝██╔██╗ ██║██║   ██║██║ █╗ ██║██║   ██║   █████╗   ╚███╔╝    ██║   
██╔══██╗██╔══╝  ██╗██║╚██╗██║██║   ██║██║███╗██║╚═╝   ██║   ██╔══╝   ██╔██╗    ██║   
██║  ██║███████╗╚═╝██║ ╚████║╚██████╔╝╚███╔███╔╝██╗   ██║   ███████╗██╔╝ ██╗   ██║   
╚═╝  ╚═╝╚══════╝   ╚═╝  ╚═══╝ ╚═════╝  ╚══╝╚══╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝   
""",start_color=[51,51,51],end_color=[61,61,61],wait=False)
    wow("终端无限，故事可见",text_color='black',wait=False)

    try:
        with open('now', 'r', encoding='utf-8') as f:
            level = f.read().strip()
            if level:
                shared_data.condition_vars = True
                set_condition_var("new_game", True)
    except FileNotFoundError:
        pass

def init():
    loading_t = threading.Thread(target=loading)
    loading_t.start()
    all_init()
    global is_loading
    is_loading = False
    ml_input()

if __name__ == "__main__":
    init()