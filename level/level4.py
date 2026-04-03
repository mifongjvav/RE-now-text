from rich.console import Console
import msvcrt
from level.libs.l4lib import image
from level.libs.init import init
init()
from galite import P, S, input_text, N  # noqa: E402
from map import GameMap  # noqa: E402

P('Argon', '欢迎回来，这是一个非常简短的教程关卡，目的是让你熟悉RNT0.5中的最新函数 image()')
P('Argon', '你可以使用它显示一张图片，24位色哦')
image("res/level4_ayyV.jpg",width=120)
P('Argon', '嗯对，没了')
S('Argon', '在 1.1.0-rc 中，我们加入了大地图引擎\n要注意他只支持 Windows\n进入：0')
if input_text[0] == "0":
    console = Console()
    def on_treasure(game_map, y, x):
        """拾取箱子获得棍母"""
        console.clear()
        console.print("✨ 你打开了一个箱子！获得了100个棍母！", style="bold yellow")
        game_map.map_data[y][x] = '地'
        console.print("\n按任意键继续...", style="dim")
        msvcrt.getch()

    def on_person(game_map, y, x):
        """与人交互后变成入，不再可交互"""
        console.clear()
        console.print("💬 人: 别烦我！", style="cyan")
        game_map.map_data[y][x] = '入'   # 变成不可交互的字符
        console.print("\n按任意键继续...", style="dim")
        msvcrt.getch()

    game = GameMap(render_distance=12)  # 视野半径5

    game.register_interactable('箱', on_treasure)
    game.register_interactable('人', on_person)

    try:
        game.run()
    except KeyboardInterrupt:
        console.clear()
        console.print("\n[yellow]游戏被中断[/yellow]")

N("level5")