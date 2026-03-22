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
from rich.traceback import install
install(show_locals=True)  # 安装 Rich 的 traceback 处理器

build_package

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    lica.unpack(
    os.path.join(base_path, "res.lica"),
    os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else base_path, "res")
)

if getattr(sys, 'frozen', False):
    # 打包成 exe 后
    log_dir = Path(sys.executable).parent
else:
    # 开发环境
    log_dir = Path(__file__).parent

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

if __name__ == "__main__":
    ml_input()
