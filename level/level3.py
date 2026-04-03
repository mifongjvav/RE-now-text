from level.libs.init import init
from level.libs.l3lib import wow, input_text_l3lib, markdown
init()
from galite import P, S, N, clear, return_value, input_text  # noqa: E402

P("Argon", "欢迎来到RE:now!text的第三关！")
P("Argon", "这是一个示例模板……停，你好像已经听腻了，那不如我们换换口味吧")
clear()
P("Argon", "伟大的RE:now!text第三关！现已开始！", hide=True)
wow(return_value[0], text_color='black')
P("Argon", "怎么样？这个效果还不错吧？")
P("Argon", "你可以使用 wow() 来改变P的显示效果，注意只有hide参数为True时才不会输出原本的对话框")
P("Argon", "第三关的目标是：使用 wow() 来改变P的显示效果，注意只有hide参数为True时才不会输出原本的对话框")
P("Argon", "你可以给 wow() 传入不同的参数来改变渐变的颜色、文字颜色、是否加粗等，试试看吧！")
P("Argon", "现在是薄荷到薰衣草！", hide=True)
wow(return_value[0], start_color=[204, 255, 229], end_color=[230, 230, 250], text_color='black')
P("Argon", "怎么样？这个颜色还不错吧？这是用Rich库实现的")
P("Argon", "你可以在Rich库的文档中找到更多关于颜色和样式的信息：https://rich.readthedocs.io/en/stable/style.html")
P("Argon", "现在给你看个高度自定义的对话框")
P("Argon", "酷不酷？\nThis is RICH!", hide=True)
wow(return_value[0], start_color=[170, 224, 242], end_color=[232, 211, 242], text_color='black', animate=True, animation_speed=0)
P("Argon", "怎么样？这个动画效果还不错吧？")
P("Argon", "你可以通过调整animate和animation_speed参数来改变动画的效果")
P("Argon", '你可能觉得这太麻烦了，实际上你可以把"l3lib.py"扔给AI让它写')
S("Argon", "到你了，你现在要实现这个对话框的样式，\n样式：[170, 224, 242]到[232, 211, 242]", hide=True)
wow(return_value[0], start_color=[170, 224, 242], end_color=[232, 211, 242], text_color='black', wait_input=True)
if input_text_l3lib[0] == "wow(return_value[0], start_color=[170, 224, 242], end_color=[232, 211, 242])":
    P("Argon", "你真棒！完全正确！")
else:
    P("Argon", "你写的代码是：\n" + input_text_l3lib[0] + "\n虽然不完全正确，但也不错了！")
P("Argon", "注意：wow的input逻辑使用l3lib里面的input_text_l3lib而非galite里面的input_text")
P("Argon", "第三关现在结束了（划掉），第三关被我续写了")
text = """
# 这是l3lib的markdown功能

太酷了！

"""
markdown(text)
P('Argon', '自0.4版本开始，你可以使用markdown函数来渲染Markdown内容文本了，\n受Rich限制，它不支持GitHub的Alerts语法')
S('Argon', '接下来，它会渲染你输入的Markdown文件')
try:
    with open(input_text[0], 'r', encoding='utf-8') as f:
        md_text = f.read()
except Exception as e:
    P('Argon', e)
    md_text = "# 错误：无法读取文件\n\n请确保文件路径正确。\n"
markdown(md_text)
P('Argon', '发明Rich的真是个天才，下一关开始你会见识到更多基于Rich的高级函数')
N('level4')