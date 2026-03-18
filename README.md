# RE:now!text v1.0.0-rc3

- **终端无限，故事可见**

最后一个测试版

> [!WARNING]
> RE:now!text还在早期开发阶段
>
> 文档字符串不全、功能缺失、写的很屎山是非常正常的事情

- [x] 基本游戏功能
- [x] 主菜单（基本实现）
- [x] 自定义制表符
- [x] 自定义样式
- [x] 打印图片
- [x] 自动化打包
- [x] 自动打包其它资源
- [ ] 真正的继续游戏
- [ ] 联机
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
from galite import P, S, A, N, E, input_text, set_theme # noqa: E402
from level.l3lib import wow, input_text_l3lib, markdown
from level.l4lib import image
```

开始前执行以上代码来初始化

| 类型 | 用途 |
| :---: | :---: |
| P | 剧情 |
| S | 选择器 |
| A | 进度 |
| N | 切换关卡 |
| E | sys.exit() |
| wow | 为对话框添加样式，注意不支持Rich主题 |
| markdown | markdown支持 |
| image | 显示图片，注意如果square为True横向分辨率会减半 |
| set_theme | 设置主题 |

其它没什么好说的，和Python一样，你可以随意搭配，放在什么目录都没人管你

## 打包

执行`build.ps1`或从资源管理器拖进终端并按下Enter

## 调试

在根目录（**注意不是关卡目录**）执行 `python -m level.无后缀关卡名`
