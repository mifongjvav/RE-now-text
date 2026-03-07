from terminaltables3 import DoubleTable
import logging
import ArgonCodeKits as ack
import sys
import subprocess

def P(title: str="undefined",text: str="undefined"):
    table_data = [[text]]
    table = DoubleTable(table_data)
    table.title = title
    logging.info(f'\n{table.table}')

def S(title: str="undefined",text: str="undefined"):
    logging.debug(f'{title}: {text}')
    table_data = [[text]]
    table = DoubleTable(table_data)
    table.title = title
    logging.info(f'\n{table.table}')
    global input_text
    input_text = ack.input()

def A(name: str="undefined",level: int=0):
    logging.debug(f'{name}: {level}')
    if level == 0:
        table_data = [f'{name}']
        table = DoubleTable(table_data)
        table.title = '进度已完成！'
        logging.info(f'\n\033[1;37;43m{table.table}\033[0m')
    elif level == 1:
        table_data = [f'{name}']
        table = DoubleTable(table_data)
        table.title = '目标已完成！'
        logging.info(f'\n\033[1;37;43m{table.table}\033[0m')
    else:
        table_data = [f'{name}']
        table = DoubleTable(table_data)
        table.title = '挑战已完成！'
        logging.info(f'\n\033[1;37;45m{table.table}\033[0m')

def N(path: str):
    subprocess.run(["python",path])

def E():
    sys.exit()