import sys
import os
import msvcrt
import time
import random
from rich.console import Console
from rich.text import Text

console = Console()

def resource_path(relative_path):
    """获取资源的绝对路径"""
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__) or '.'
    return os.path.join(base_path, relative_path)

def generate_map(width=72, height=72, seed=None):
    """
    生成随机地图
    使用简单的随机权重生成地面、石头、箱子、人
    权重: 地(10), 石(5), 箱(1), 人(2)
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()
    
    items = ['地', '石', '箱', '人']
    weights = [10, 5, 1, 2]
    
    # 创建空地图
    map_data = []
    for _ in range(height):
        row = random.choices(items, weights=weights, k=width)
        map_data.append(row)
    
    # 确保至少有一个出生点，放在地图中心附近
    center_y, center_x = height // 2, width // 2
    map_data[center_y][center_x] = '出'
    
    return map_data, center_y, center_x

class GameMap:
    """
    游戏地图类，封装地图加载、显示、移动、交互等逻辑
    """
    def __init__(self, render_distance: int = 5, map_data=None, start_pos=None):
        """
        :param render_distance: 视野半径（显示以玩家为中心的方形区域边长 = 2*rd+1）
        :param map_data: 可选，二维字符列表，若为None则随机生成72x72地图
        :param start_pos: 可选，起始位置 [y, x]，若为None则使用地图中的'出'或中心
        """
        self.render_distance = render_distance
        self.map_data = map_data
        self.height = 0
        self.width = 0
        self.player_pos = [0, 0]
        self.interactable_chars = {}   # 可交互字符及其动作
        
        # 地图矩形边界（用于距离计算）
        self.map_min_row = 0
        self.map_max_row = 0
        self.map_min_col = 0
        self.map_max_col = 0
        
        if self.map_data is None:
            # 随机生成地图
            self.map_data, start_y, start_x = generate_map()
            self.height = len(self.map_data)
            self.width = len(self.map_data[0])
            self.player_pos = [start_y, start_x]
            # 设置边界（重要！修复红色玩家问题）
            self.map_min_row = 0
            self.map_max_row = self.height - 1
            self.map_min_col = 0
            self.map_max_col = self.width - 1
        else:
            self._load_from_data(start_pos)
    
    def _load_from_data(self, start_pos):
        """从给定的二维列表加载地图"""
        self.height = len(self.map_data)
        self.width = max(len(row) for row in self.map_data) if self.map_data else 0
        # 确保每行长度一致（用空格填充）
        for y, row in enumerate(self.map_data):
            if len(row) < self.width:
                self.map_data[y] = row + [' '] * (self.width - len(row))
        
        # 寻找起始点
        if start_pos is not None:
            self.player_pos = list(start_pos)
        else:
            found = False
            for y in range(self.height):
                for x in range(self.width):
                    if self.map_data[y][x] == '出':
                        self.player_pos = [y, x]
                        found = True
                        break
                if found:
                    break
            if not found:
                # 默认中心
                self.player_pos = [self.height // 2, self.width // 2]
        
        # 更新矩形边界
        self.map_min_row = 0
        self.map_max_row = self.height - 1
        self.map_min_col = 0
        self.map_max_col = self.width - 1
    
    def register_interactable(self, char: str, action_func):
        """注册可交互字符及其动作"""
        self.interactable_chars[char] = action_func
    
    def is_inside_map(self, y, x):
        """判断坐标是否在地图内"""
        return 0 <= y < self.height and 0 <= x < self.width
    
    def get_distance_to_map_boundary(self, y, x):
        """计算坐标到地图矩形边界的曼哈顿距离"""
        dy = 0
        if y < self.map_min_row:
            dy = self.map_min_row - y
        elif y > self.map_max_row:
            dy = y - self.map_max_row
        dx = 0
        if x < self.map_min_col:
            dx = self.map_min_col - x
        elif x > self.map_max_col:
            dx = x - self.map_max_col
        return dy + dx
    
    def get_towards_map_direction(self, y, x):
        """返回指向地图内的方向 (dy, dx)"""
        dy, dx = 0, 0
        if y < self.map_min_row:
            dy = 1
        elif y > self.map_max_row:
            dy = -1
        if x < self.map_min_col:
            dx = 1
        elif x > self.map_max_col:
            dx = -1
        if dy != 0:
            return dy, 0
        if dx != 0:
            return 0, dx
        return 0, 0
    
    def get_player_color(self):
        """根据到地图边界的距离返回颜色"""
        dist = self.get_distance_to_map_boundary(*self.player_pos)
        # 调试输出
        console.print(f"Debug: player_pos={self.player_pos}, map_max_row={self.map_max_row}, map_max_col={self.map_max_col}, dist={dist}")
        return "bold red" if dist >= 1 else "bold yellow"
    
    def get_brightness(self, y, x):
        """亮度基于到玩家的曼哈顿距离"""
        distance = abs(y - self.player_pos[0]) + abs(x - self.player_pos[1])
        max_distance = self.render_distance * 2
        if distance > max_distance:
            return 0.0
        brightness = 1.0 - (distance / max_distance)
        return max(0.0, min(1.0, brightness))
    
    def get_style_and_char(self, y, x):
        """返回 (字符, 样式)"""
        # 玩家位置
        if y == self.player_pos[0] and x == self.player_pos[1]:
            return "我", self.get_player_color()
        
        # 地图内格子
        if self.is_inside_map(y, x):
            char = self.map_data[y][x]
            brightness = self.get_brightness(y, x)
            if char in self.interactable_chars:
                if brightness < 0.3:
                    return char, "dim cyan"
                return char, "bold cyan"
            if brightness >= 0.8:
                return char, "white"
            elif brightness >= 0.6:
                return char, "bright_white"
            elif brightness >= 0.4:
                return char, "white"
            elif brightness >= 0.2:
                return char, "black on white"
            else:
                return char, "black on black"
        
        # 地图外格子
        dist = self.get_distance_to_map_boundary(y, x)
        if dist >= 2:
            return "无", "black on red"
        else:
            return "无", "black on black"
    
    def render_map_text(self):
        """生成显示文本（玩家居中）"""
        cam_y, cam_x = self.player_pos
        rd = self.render_distance
        y_start = cam_y - rd
        y_end = cam_y + rd + 1
        x_start = cam_x - rd
        x_end = cam_x + rd + 1
        
        full_text = Text()
        for y in range(y_start, y_end):
            line = Text()
            for x in range(x_start, x_end):
                ch, style = self.get_style_and_char(y, x)
                line.append(ch, style=style)
            full_text.append(line)
            full_text.append("\n")
        return full_text
    
    def show_map(self):
        """显示地图"""
        console.clear()
        console.print()  # 空行避免顶部遮挡
        console.print(self.render_map_text())
        y, x = self.player_pos
        char = self.map_data[y][x] if self.is_inside_map(y, x) else "无"
        dist = self.get_distance_to_map_boundary(y, x)
        console.print(f"位置: ({y}, {x})  脚下: {char}  距地图边界: {dist}", style="dim")
        console.print("WASD移动 | F交互 | Q退出", style="green")
    
    def move_player(self, dy, dx):
        """手动移动（不带拉回）"""
        self.player_pos[0] += dy
        self.player_pos[1] += dx
        return True
    
    def interact(self):
        """与当前脚下字符交互"""
        y, x = self.player_pos
        if self.is_inside_map(y, x):
            char = self.map_data[y][x]
            if char in self.interactable_chars:
                action = self.interactable_chars[char]
                action(self, y, x)
                return True
        return False
    
    def run(self):
        """主游戏循环，处理移动和拉回"""
        console.clear()
        console.print("[bold yellow]游戏开始！[/bold yellow]", justify="center")
        console.print(f"视野范围: {self.render_distance}\n", justify="center")
        self.show_map()
        
        last_pull_time = 0
        pull_interval = 0.01   # 拉回间隔（秒）
        last_key_time = 0       # 上次按键处理时间
        key_delay = 0.15        # 按键延迟（秒），防止一次按键触发多次移动
        
        while True:
            now = time.time()
            # 自动拉回（距离≥2时）
            dist = self.get_distance_to_map_boundary(*self.player_pos)
            if dist >= 2 and now - last_pull_time >= pull_interval:
                dy, dx = self.get_towards_map_direction(*self.player_pos)
                if dy != 0 or dx != 0:
                    self.player_pos[0] += dy
                    self.player_pos[1] += dx
                    self.show_map()
                last_pull_time = now
            
            # 处理键盘输入
            if msvcrt.kbhit():
                # 限制按键处理频率
                if now - last_key_time >= key_delay:
                    key = msvcrt.getch().decode('ascii', errors='ignore').lower()
                    moved = False
                    if key == 'w':
                        self.move_player(-1, 0)
                        moved = True
                    elif key == 's':
                        self.move_player(1, 0)
                        moved = True
                    elif key == 'a':
                        self.move_player(0, -1)
                        moved = True
                    elif key == 'd':
                        self.move_player(0, 1)
                        moved = True
                    elif key == 'f':
                        self.interact()
                        self.show_map()
                    elif key == 'q':
                        console.clear()
                        console.print("[yellow]游戏结束！[/yellow]")
                        break
                    
                    if moved:
                        self.show_map()
                        last_pull_time = time.time()
                        last_key_time = now
            