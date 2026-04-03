from level.libs.init import init
import threading
from level.libs.audio import SpatialAudioPlayer
import time
init()
from galite import P  # noqa: E402
import Main  #noqa: E402

P("Argon","欢迎回来，自 1.2.0-rc 开始，我们加入了加载进度")
P("Argon","他可以在 Windows 终端 上显示加载进度条，使用缓动效果\n要注意这个进度条是不确定性的，如果要精确数值，请改用Rich")
P("Argon","注意终端的左上角和任务栏")
loading_t = threading.Thread(target=Main.loading)
loading_t.start()
time.sleep(5)
Main.is_loading = False
P("Argon","怎么样？")
P("Argon", "我们在1.2.0-rc2中，加入了音频播放，它甚至支持空间音频，你可以试试看")
# 创建播放器
player = SpatialAudioPlayer()

# 立体声模式
player.load('res/dadadadadaru.mp3')
player.play()

# 等待播放完成
while player.is_playing:
    time.sleep(0.1)