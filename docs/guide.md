# RE:now!text 使用指南

## 介绍

一个轻量级的终端视觉小说引擎，兼容性强、速度快、跨平台

## 快速开始

### 安装方式

```bash
git clone https://github.com/mifongjvav/RE-now-text.git
cd RE-now-text
```

## 快速学习

```bash
python Main.py
```

观看完所有教学关卡

## 编写第一个关卡

### 核心概念

#### 对话框系统

`P()` 和 `S()` 函数

`P()`  和 `S()` 可以显示一个对话框，为它添加`title`和`text`参数即可更改内容

`S()` 在显示完后会进入输入状态，输入的内容会保存到input_text[0]

它们俩都有 `theme` 和 `hide` 参数，前者用于设置主题，后者用于隐藏这次显示的对话框

#### 进度系统

我们拥有与《Minecraft:Java Edition》类似的进度系统

你可以使用 `A()` 来让玩家获取进度，为它指定`name`和`level`参数来指定进度内容与样式

`name`参数指定了进度的名字，`level`则定义了进度的等级，分别为：

| 数字 | 等级 |
| :-: | :-: |
| 0 | 进度 |
| 1 | 目标 |
| 2 | 挑战 |

### 普通概念

#### 切换关卡

`N()` 可以用于切换关卡，参数填关卡名就行了

#### 退出

`E()` 用于退出，参数是状态码，可以不填

### 额外概念

#### 主题系统

你可能注意到了`set_theme`，它含有以下主题：

| 主题 | 名字 |
| :-: | :-: |
| rounded | Rich UI |
| double | 双线框 |
| single | 单线框 |
| ascii | ASCII |

除非需要，否则我们只推荐你使用`rounded`或`single`

#### 个性化

你可能发现了`l3lib`和`l4lib`，它们都是美化终端的好帮手

##### wow()

这个函数可以美化对话框，参数在文档字符串里面写的非常详细

> [!WARNING]
> 此函数仅支持`terminaltables3`系列主题

##### markdown()

显示一个markdown内容，你应该会用

##### image()

显示一张图片，你也应该会用

### 特殊

#### 大地图引擎

这是一个实验性功能，它类似于[文字游戏](https://store.steampowered.com/app/1109570/)

默认使用`72x72`大小的地图，内容完全随机生成，具体可在`map.py`中的`generate_map`函数更改

#### 不确定值进度条

让 `Windows 终端` 显示一个不确定值的进度条在窗口与任务栏

> [!WARNING]
> 你不应该把它放在主线程里面运行，因此，你应该这么写：
>
> ```python
> import Main  #noqa: E402
> loading_t = threading.Thread(target=Main.loading)
> loading_t.start()
> Main.is_loading = False
> ```
>
> 注意：并不需要 `join()` 该线程

示例：
![example](https://db0l8fnn8oqtof.database.nocode.cn/storage/v1/object/public/wenjian/anonymous/1774684778651_17q30xejdbhh.png)

### 高级

#### 音频播放

```python
player = SpatialAudioPlayer()
player.load('文件位置')
player.play()
```

这是一个简单的示例，但实际上，它支持 `HRTF` 和 `VBAP` 音频播放

## 使用Markdown编写关卡

在 `1.2.0-rc3`，我们加入了M2G，你可以使用Markdown来编写关卡，更简单，更快

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
