# RE:now!text v1.2.0

- **终端无限，故事可见**

最后亿个测试版

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
- [x] 大地图引擎
- [x] 不确定值进度条
- [x] Nuitka打包
- [x] 音频播放
- - [x] 空间音频
- - - [x] HRTF音频
- - - [x] VBAP音频
- [x] 使用Markdown编写关卡
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
from level.libs.init import init
init()
from galite import P, S, A, N, E, input_text, set_theme # noqa: E402
from level.libs.l3lib import wow, input_text_l3lib, markdown
from level.libs.l4lib import image
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

如果你希望它更快，更安全，请执行`build-Nuitka.ps1`或从资源管理器拖进终端并按下Enter

## 调试

在根目录（**注意不是关卡目录**）执行 `python -m level.无后缀关卡名`

## M2G 转译器

M2G 可以将 Markdown 剧本自动转换为 RNT Python 代码，让编剧无需学习Python也可以创作出好剧情。

### 支持的语法

```markdown
# 标题               → 作为注释保留，用于章节标记

> 注释               → 转换为 Python 注释

- 角色名             → 切换当前说话角色
- 全称<别名1,别名2...   → 注册角色及别名（不切换角色）

普通文本             → 转换为 P("角色名", "文本")

S<提示文本          → 转换为 S("角色名", "提示文本")

A<成就名<等级       → 转换为 A("成就名", 等级)

N<关卡名            → 转换为 N("关卡名")

exit<<状态码        → 转换为 E(状态码)

```python
# Python 代码块
wow("渐变文字")
markdown("# 标题")
```

### 示例剧本

```markdown
# md/level1

> 定义角色

- Argon<argon,arg

> 使用别名

- arg

欢迎来到 RNT 引擎！

S<你叫什么名字？

- Argon

你好，{input_text[0]}！

A<初次见面<0

N<level2

```

### 转换结果

运行 `python Main.py --RNT --M2G 目录` 后，自动生成关卡到 `level/`，可直接被 RNT 引擎加载。
