import logging
from logging import error
from rich import print
from json import load
from os import path, _exit
import shared_data
from shared_data import condition_vars
import sys
from subprocess import run
from MenuLite.Menu.MenuFunc import *  # noqa: F403
from level.l3lib import markdown
import requests
from galite import main_menu_p, set_theme
import coloredlogs
from rich.traceback import install
install(show_locals=True)  # 安装 Rich 的 traceback 处理器

coloredlogs.install(
    level='WARNING', 
    fmt="%(message)s"
)

notice = requests.get(
    "https://gh.llkk.cc/https://raw.githubusercontent.com/mifongjvav/mifongjvav/refs/heads/main/RNT_msg.md"
).text
markdown(notice, wait=False)
logging.warning(
    "\n警告：RE:now!text还处于极早期测试阶段，出现任何bug都是很正常的\n出现bug请反馈：https://github.com/mifongjvav/RE-now-text/issues/new"
)


def get_config_path():
    """获取配置文件的正确路径（兼容打包环境）"""
    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", path.dirname(sys.executable))
    else:
        base_path = path.dirname(path.abspath(__file__))

    return path.join(base_path, "Menu", "MlConfig.json")


# 获取配置路径并加载
config_path = get_config_path()

try:
    with open(config_path, encoding="utf-8") as file:
        config = load(file)
except FileNotFoundError:
    error(f"配置文件未找到: {config_path}")
    error("请确保打包时已添加配置文件，或检查文件路径")
    sys.exit(1)

menu_items = config["menu_items"]


def check_conditions(conditions):
    if not conditions:
        return True, None
    for key, required_value in conditions.items():
        current_value = condition_vars.get(key)
        if current_value != required_value:
            return False, {key: required_value}
    return True, None

set_theme('rounded')

def ml_main_menu():
    menu_list = []
    for key, item_info in menu_items.items():
        item_name = item_info.get("name", "未命名菜单项")
        conditions = item_info.get("conditions", {})
        conditions_met, _ = check_conditions(conditions)
        if conditions_met:
            menu_list.append([f"{key}. {item_name}"])
    menu_list.append(["x. 退出"])
    menu_list.append(["re. 重启"])
    main_menu_p('主菜单', menu_list)

def ml_input():
    while True:
        try:
            ml_main_menu()
            print("请输入菜单项: ")
            user_input = input().strip()

            if user_input == "x":
                print("退出程序")
                sys.exit(0)
            elif user_input == "re":
                run([sys.executable] + sys.argv + ["--restart"])
                sys.exit(0)

            if user_input in menu_items:
                item_info = menu_items[user_input]
                item_name = item_info.get("name", "未命名菜单项")
                func_name = item_name

                conditions = item_info.get("conditions", {})
                conditions_met, failed_condition = check_conditions(conditions)

                if not conditions_met:
                    failed_key, required_value = next(iter(failed_condition.items()))
                    current_value = condition_vars.get(failed_key, "未设置")
                    error(f"功能 '{item_name}' 受到限制")
                    error(
                        f"条件不满足: {failed_key} 需要为 '{required_value}'，当前为 '{current_value}'"
                    )
                    print("请先满足条件后再使用此功能")
                    continue

                func = globals().get(func_name)

                if func and callable(func):
                    print(f"执行功能: {item_name}")
                    func()
                else:
                    error(f"函数 {func_name} 不存在或不可调用")
            else:
                error(f"无效的键: {user_input}")
        except KeyboardInterrupt:
            print("\n用户中断操作")
            _exit(0)
        except Exception as e:
            import traceback

            error(f"发生错误: {str(e)}")
            traceback.print_exc()


def set_condition_var(key, value):
    condition_vars[key] = value


def show_condition_vars():
    print("当前条件变量状态:")
    for key, value in condition_vars.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    if not hasattr(shared_data, "condition_vars"):
        shared_data.condition_vars = {}

    ml_input()
