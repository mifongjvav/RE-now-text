from level.init import init
init()
from galite import P, E  # noqa: E402
from level.l4lib import image  # noqa: E402

P('Argon', '欢迎回来，这是一个非常简短的教程关卡，目的是让你熟悉RNT0.5中的最新函数 image()')
P('Argon', '你可以使用它显示一张图片，24位色哦')
image("image/level4_ayyV.jpg",width=1280)
P('Argon', '嗯对，没了')
E()