from level.init import init
import threading
import time
init()
from galite import P  # noqa: E402
import Main  #noqa: E402

P("Argon","欢迎回来，自1.2.0-rc开始，我们加入了加载进度")
P("Argon","他可以在 Windows 终端 上显示加载进度条，使用缓动效果\n要注意这个进度条是不确定性的，如果要精确数值，请改用Rich")
P("Argon","注意终端的左上角和任务栏")
loading_t = threading.Thread(target=Main.loading)
loading_t.start()
time.sleep(5)
Main.is_loading = False
P("Argon","怎么样？")