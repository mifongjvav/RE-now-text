import subprocess
import shared_data

def 开始新游戏():
    from MenuLite.MlMain import set_condition_var
    shared_data.condition_vars = True
    set_condition_var("new_game", True)
    with open('now', 'w', encoding='utf-8') as f:
        f.write('level1')
    subprocess.run(["python", "./level/level1.py"])

def 继续游戏():
    with open ('now', 'r', encoding='utf-8') as f:
        level = f.read().strip()
    subprocess.run(["python", f"./level/{level}.py"])

def 进度():
    with open('advancements', 'r', encoding='utf-8') as f:
        advancements = f.read().strip()
    if advancements:
        name, level = advancements.split(':')
        if level == '0':
            print(f'\n\033[1;37;43m进度：{name}\033[0m')
        elif level == '1':
            print(f'\n\033[1;37;43m目标：{name}\033[0m')
        elif level == '2':
            print(f'\n\033[1;37;45m挑战：{name}\033[0m')
    else:
        print('没有进度')

def 设置():
    pass