import shared_data
import importlib


def 开始新游戏():
    from MenuLite.MlMain import set_condition_var

    shared_data.condition_vars = True
    set_condition_var("new_game", True)
    with open("now", "w", encoding="utf-8") as f:
        f.write("level1")
    importlib.import_module("level.level1")


def 继续游戏():
    with open("now", "r", encoding="utf-8") as f:
        level = f.read().strip()
    importlib.import_module(f"level.{level}")


def 进度():
    try:
        with open("advancements", "r", encoding="utf-8") as f:
            lines = f.readlines()

        if lines:
            for line in lines:
                line = line.strip()
                if line:  # 跳过空行
                    parts = line.split(":")
                    if len(parts) >= 2:
                        name = parts[0]
                        level = parts[1]

                        if level == "0":
                            print(f"\033[1;37;43m进度：{name}\033[0m")
                        elif level == "1":
                            print(f"\033[1;37;43m目标：{name}\033[0m")
                        elif level == "2":
                            print(f"\033[1;37;45m挑战：{name}\033[0m")
                        else:
                            print(f"未知等级：{name}")
        else:
            print("没有进度")
    except FileNotFoundError:
        print("没有进度文件，请先开始新游戏")
    except Exception as e:
        print(f"读取进度时发生错误: {e}")


def 设置():
    pass
