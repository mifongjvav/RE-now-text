import webbrowser
from level.init import init
init()
from galite import P, S, A, N, input_text, set_theme # noqa: E402

P('Argon','欢迎来到RE:now!text的第二关！')
P('Argon','这是一个示例模板，为了让你获得一些制作游戏的灵感')
P('Argon','在这个关卡里，你可以随意发挥，\n使用P函数输出文本，使用S函数获取输入，使用A函数记录进度，使用N函数跳转关卡，使用E函数退出游戏')
P('Argon','你可以在这个关卡里制作一个小型的Galgame，或者一个小型的冒险游戏，或者一个小型的解谜游戏，甚至是一个小型的RPG游戏！')

S('Argon','你可以输入任何python代码，解释器会执行它，我没有屏蔽一些危险代码，但你也别犯傻')
run = input_text[0]
try:
    exec(run)
except Exception as e:
    P('Argon',f'执行代码时发生了错误：{e}，你是杂鱼吗？会不会写代码？')
S('Argon','你喜欢什么主题？在前面的关卡中已经介绍了唯三的主题，你可以使用序号来选择它，\n分别是：\n0. single\n1. double\n2. ascii')
theme_choice = input_text[0]
if theme_choice == '0':
    set_theme('single')
elif theme_choice == '1':
    set_theme('double')
elif theme_choice == '2':
    set_theme('ascii')
else:
    theme_choice = '1'
    P('Argon','你在做什么？')
P('Argon',f'现在的主题是 {["single","double","ascii"][int(theme_choice)]} 了！')
P('Argon','你玩到现在，有没有想问我是谁？')
P('Argon','我是Argon，你的引导者，也是这个世界的创造者')
P('Argon','我创造了这个世界，你是从一个名为"run"的入口来的流浪者，\n我希望你能在这个世界里找到属于自己的乐趣，\n无论是制作游戏，还是玩游戏，还是其他什么事情')
S('Argon','你想了解我的联系方式吗？输入0不要，1要')
if input_text[0] == '0':
    pass
elif input_text[0] == '1':
    P('Argon','我的邮箱是：smmomm@126.com，你再按下回车，你就会跳转过去')
    webbrowser.open("mailto:smmomm@126.com")
else:
    P('Argon','你在做什么？')
P('Argon','你有没有想过一个问题')
S('Argon','你玩这么久了，我居然没有给你任何一个真正的进度，简直可笑，\n你现在可以输入任何内容，并且获得这个进度的 进度/目标/挑战 形式，\n我们没有联网内容审核，不要害怕\n要注意我使用的制表符UI库好像有点bug，进度获得时可能会丢失标题，不过标题只有装饰作用，你不需要在意')
for i in range(3):
    A(input_text[0], i)
P('Argon','我发现Ruff烦死了，一直提示`galite.E` imported but unused Ruff(F401) [行 4，列 29]，\n接下来，会退出')
P('Argon','你被骗了，我根本没导入E')
P('Argon','第二关现在结束了，接下来会前往第三关')
N('level3')