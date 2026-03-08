# RE:now!text Alpha0.2

致力于做最好的纯命令行Galgame引擎

> [!WARNING]
> RE:now!text还在极早期开发阶段，以下为功能列表

- [x] 基本游戏功能
- [x] 主菜单（基本实现）
- [x] 自定义制表符
- [ ] 其它...

## 安装依赖

```bash
pip install -r requirements.txt
```

## 开发剧情

游戏默认会尝试运行./level/level1.py

```python
from init import init
init()
from galite import *  # noqa: F403
```

运行前必须执行以上代码来初始化

| 类型 | 用途 |
| :---: | :---: |
| P | 剧情 |
| S | 选择器 |
| A | 进度 |
| N | 切换关卡 |
| E | sys.exit() |

其它没什么好说的，和Python一样，你可以随意搭配，放在什么目录都没人管你
