# RE:now!text Alpha0.1

致力于做最好的纯命令行Galgame引擎

> [!WARNING]
> RE:now!text还在极早期开发阶段，以下为功能列表

- [x] 基本游戏功能
- [ ] 主菜单（未完全实现）
- [ ] 自定义制表符
- [ ] 其它...

## 安装依赖

```bash
pip install -r requirements.txt
```

## 开发剧情

游戏默认会尝试运行./level/level1.py

```python
import sys
import os
import ArgonCodeKits as ack
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from galite import *  # noqa: F403
ack.init_log_file("INFO")
```

替换`level1.py`的内容，头部不可变

| 类型 | 用途 |
| :---: | :---: |
| P | 剧情 |
| S | 选择器 |
| A | 进度 |
| N | 切换关卡 |
| E | sys.exit() |

其它没什么好说的，和Python一样，你可以随意搭配，放在什么目录都没人管你
