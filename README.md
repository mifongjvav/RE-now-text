# RE:now!text Alpha0.4

致力于做最好的纯命令行Galgame引擎

> [!WARNING]
> RE:now!text还在极早期开发阶段，以下为功能列表

- [x] 基本游戏功能
- [x] 主菜单（基本实现）
- [x] 自定义制表符
- [x] 自定义样式
- [x] 打包为exe
- [ ] 其它...

## 安装依赖

```bash
pip install -r requirements.txt
```

## 开发剧情

游戏默认会尝试运行./level/level1.py

```python
from level.init import init
init()
from galite import P, S, A, E, input_text, set_theme # noqa: E402
from level.l3lib import wow, input_text_l3lib
```

开始前执行以上代码来初始化

| 类型 | 用途 |
| :---: | :---: |
| P | 剧情 |
| S | 选择器 |
| A | 进度 |
| N | 切换关卡 |
| E | sys.exit() |
| wow | 使用Rich为对话框添加样式 |

其它没什么好说的，和Python一样，你可以随意搭配，放在什么目录都没人管你

## 使用pyinstaller打包为exe

执行`build.ps1`或从资源管理器拖进终端并按下Enter

## 调试

在根目录（**注意不是关卡目录**）执行`python -m level.无后缀关卡名`
