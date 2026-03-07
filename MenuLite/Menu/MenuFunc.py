import logging
import subprocess
import shared_data

def 开始新游戏():
    from MenuLite.MlMain import set_condition_var
    logging.info("开始新游戏")
    shared_data.condition_vars = True
    set_condition_var("new_game", True)
    with open('now', 'w', encoding='utf-8') as f:
        f.write('level1')
    subprocess.run(["python", "./level/level1.py"])
