from MenuLite.MlMain import ml_input
from MenuLite.MlMain import set_condition_var
import time
import shared_data

if time.time() == 1: # 骗过pyinstaller的静态分析，确保在打包所有关卡模块并且不执行
    import level.level1  # noqa: F401
    import level.level2  # noqa: F401
    import level.level3  # noqa: F401
    import level.init  # noqa: F401
    import level.l3lib  # noqa: F401

try:
    with open('now', 'r', encoding='utf-8') as f:
        level = f.read().strip()
        if level: # 如果文件里有内容，说明之前玩过
            shared_data.condition_vars = True
            set_condition_var("new_game", True)
except FileNotFoundError:
    pass

if __name__ == "__main__":
    ml_input()
