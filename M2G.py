#!/usr/bin/env python3
"""
RNT Markdown 转译器
将 Markdown 剧本转译为 RNT Python 代码
"""

# 默认配置
DEFAULT_CONFIG = {"encoding": "utf-8", "default_output": "output.py", "indent": "    "}


def parse_markdown(content: str) -> list:
    """
    解析 Markdown 内容，返回代码行列表
    """
    lines = content.split("\n")
    code_lines = []
    
    # 角色映射表：别名 -> 全称
    char_map = {}

    current_char = None
    in_code_block = False
    code_block = []

    for line in lines:
        # 处理 Python 代码块
        if line.strip().startswith("```python"):
            in_code_block = True
            code_block = []
            continue
        elif line.strip().startswith("```") and in_code_block:
            in_code_block = False
            for code_line in code_block:
                if code_line.strip():
                    code_lines.append(code_line)
                else:
                    code_lines.append("")
            code_lines.append("")
            continue
        elif in_code_block:
            code_block.append(line)
            continue

        # 跳过空行
        if not line.strip():
            code_lines.append("")
            continue

        # 注释（> 开头）
        if line.lstrip().startswith(">"):
            comment = line.lstrip()[1:].lstrip()
            code_lines.append(f"# {comment}")
            continue

         # 角色定义（- 全称<别名1,别名2,别名3）
        if line.lstrip().startswith('-') and '<' in line:
            parts = line.lstrip()[1:].split('<')
            full_name = parts[0].strip()
            alias_part = parts[1].strip() if len(parts) > 1 else ""
            
            # 注册全称
            char_map[full_name.lower()] = full_name
            
            # 注册别名
            aliases = []
            if alias_part:
                aliases = [a.strip() for a in alias_part.split(',')]
                for alias in aliases:
                    char_map[alias.lower()] = full_name
            
            # 添加注释到代码中（不执行任何操作）
            alias_list = ", ".join(aliases) if aliases else "无"
            code_lines.append(f"# 注册角色: {full_name} (别名: {alias_list})")
            continue
        
        # 角色切换（- 别名 或 - 全称）
        if line.lstrip().startswith('-'):
            char_name = line.lstrip()[1:].lstrip()
            # 查找角色（大小写不敏感）
            char_lower = char_name.lower()
            if char_lower in char_map:
                current_char = char_map[char_lower]
                # 添加注释，不生成实际代码
                code_lines.append(f"# 切换角色: {char_name} -> {current_char}")
            else:
                # 未识别的角色，输出警告并跳过
                code_lines.append(f"# [错误] 未识别的角色: '{char_name}'，请先使用 -全称<别名 定义")
                current_char = None
            continue

        # 选择器 S<内容
        if line.lstrip().startswith("S<"):
            content_text = line.lstrip()[2:].lstrip()
            char_name = current_char if current_char else "System"
            # 修复：S 函数不返回值，直接调用，然后使用 input_text[0]
            code_lines.append(f'S("{char_name}", "{content_text}")')
            continue

        # 成就 A<名字<等级
        if line.lstrip().startswith("A<"):
            parts = line.lstrip()[2:].split("<")
            if len(parts) >= 2:
                name = parts[0].strip()
                level = parts[1].strip()
                code_lines.append(f'A("{name}", {level})')
            continue

        # 切换关卡 N<关卡名
        if line.lstrip().startswith("N<"):
            level_name = line.lstrip()[2:].lstrip()
            code_lines.append(f'N("{level_name}")')
            continue

        # 退出 exit<<状态码
        if line.lstrip().startswith("exit<<"):
            code = line.lstrip()[5:].lstrip() or "0"
            # 修复：确保 code 是有效的数字
            try:
                int(code)
            except ValueError:
                code = "0"
            code_lines.append(f"E({code})")
            continue

        # 标题（# 或 ## 开头）
        if line.lstrip().startswith("#"):
            # 保留原始标题（包括 # 的数量）
            code_lines.append(line.lstrip())
            continue

          # 普通对话
        if current_char and line.strip():
            text = line.strip()
            text = text.replace('"', '\\"')
            # 添加注释说明当前角色
            code_lines.append(f"# 对话 ({current_char})")
            if '{input_text[0]}' in text or '{input_text}' in text:
                text = text.replace('{input_text[0]}', '{input_text[0]}')
                text = text.replace('{input_text}', '{input_text[0]}')
                code_lines.append(f'P("{current_char}", f"{text}")')
            else:
                code_lines.append(f'P("{current_char}", "{text}")')
            continue

        # 无法识别的行，当作注释处理
        if line.strip():
            code_lines.append(f"# [未识别] {line}")

    return code_lines


def convert(markdown_content: str, config: dict = None) -> str:
    """
    将 Markdown 内容转换为 RNT Python 代码

    参数:
        markdown_content: Markdown 字符串
        config: 配置字典（可选）

    返回:
        Python 代码字符串
    """
    if config is None:
        config = DEFAULT_CONFIG

    code_lines = [
        "# 这是一个通过 M2G 从 Markdown 转译 到RNT Python 的关卡",
        """
from galite import P,S,A,N,E,input_text,return_value,set_theme,clear,enter_is_text # noqa
from level.libs.l4lib import image # noqa
from level.libs.l3lib import wow,markdown,input_text_l3lib # noqa
""",
        "",
        "",
    ]

    # 解析 Markdown
    parsed_lines = parse_markdown(markdown_content)

    # 合并代码
    code_lines.extend(parsed_lines)

    return "\n".join(code_lines)


def convert_file(input_path: str, output_path: str = None, config: dict = None) -> bool:
    """
    将 Markdown 文件转换为 RNT Python 文件

    参数:
        input_path: 输入的 Markdown 文件路径
        output_path: 输出的 Python 文件路径（可选）
        config: 配置字典（可选）

    返回:
        成功返回 True，失败返回 False
    """
    if config is None:
        config = DEFAULT_CONFIG

    # 读取输入文件
    try:
        with open(input_path, "r", encoding=config.get("encoding", "utf-8")) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误: 文件 '{input_path}' 不存在")
        return False
    except Exception as e:
        print(f"错误: 无法读取文件 '{input_path}': {e}")
        return False

    # 转换
    python_code = convert(content, config)

    # 确定输出路径
    if output_path is None:
        output_path = config.get("default_output", "output.py")

    # 写入输出文件
    try:
        with open(output_path, "w", encoding=config.get("encoding", "utf-8")) as f:
            f.write(python_code)
        print(f"✅ 转换成功: {input_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"错误: 无法写入文件 '{output_path}': {e}")
        return False
