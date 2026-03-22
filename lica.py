import json
import base64
import os
from typing import Dict, List, Union

try:
    import ijson

    HAS_IJSON = True
except ImportError:
    HAS_IJSON = False


def _load_lica(lica_path: str) -> dict:
    """加载整个 lica 文件到字典（用于修改操作）"""
    try:
        with open(lica_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise IOError(f"读取 lica 文件失败: {e}")


def _save_lica(lica_path: str, data: dict) -> None:
    """将字典保存为 lica 文件（格式化为易读形式）"""
    try:
        with open(lica_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise IOError(f"写入 lica 文件失败: {e}")


def pack_directory(lica_path: str, source_dir: str) -> int:
    """
    将整个目录打包为 lica 文件（覆盖已存在的文件）。

    :param lica_path: 输出的 lica 文件路径
    :param source_dir: 要打包的源目录
    :return: 打包的文件数量
    """
    source_dir = os.path.abspath(source_dir)
    if not os.path.isdir(source_dir):
        raise NotADirectoryError(f"源目录不存在: {source_dir}")

    data = {}
    file_count = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, source_dir).replace(os.sep, "/")
            try:
                with open(full_path, "rb") as f:
                    content = f.read()
                data[rel_path] = base64.b64encode(content).decode("utf-8")
                file_count += 1
                if file_count % 100 == 0:
                    print(f"已处理 {file_count} 个文件...")
            except Exception as e:
                print(f"警告：跳过文件 {full_path}，原因: {e}")

    _save_lica(lica_path, data)
    print(f"✅ 打包完成：{file_count} 个文件 -> {lica_path}")
    return file_count


def unpack(lica_path: str, output_dir: str, stream: bool = True) -> int:
    """
    将 lica 文件解包到指定目录。

    :param lica_path: 输入的 lica 文件路径
    :param output_dir: 输出目录（自动创建）
    :param stream: 是否使用流式解析（需要 ijson，若未安装则自动降级）
    :return: 解包的文件数量
    """
    os.makedirs(output_dir, exist_ok=True)

    if stream and HAS_IJSON:
        # 流式解析（适合超大文件）
        try:
            with open(lica_path, "rb") as f:
                parser = ijson.kvitems(f, "")
                count = 0
                for key, b64_str in parser:
                    try:
                        content = base64.b64decode(b64_str)
                        full_path = os.path.join(output_dir, key)
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        with open(full_path, "wb") as out_f:
                            out_f.write(content)
                        count += 1
                        if count % 100 == 0:
                            print(f"已解包 {count} 个文件...")
                    except Exception as e:
                        print(f"警告：处理文件 {key} 时出错: {e}")
                return count
        except Exception as e:
            print(f"流式解析失败，降级为标准加载: {e}")
            # 降级到标准加载

    # 标准一次性加载（备选）
    try:
        with open(lica_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise IOError(f"读取 lica 文件失败: {e}")

    count = 0
    for rel_path, b64_str in data.items():
        try:
            content = base64.b64decode(b64_str)
            full_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "wb") as out_f:
                out_f.write(content)
            count += 1
            if count % 100 == 0:
                print(f"已解包 {count} 个文件...")
        except Exception as e:
            print(f"警告：处理文件 {rel_path} 时出错: {e}")
    print(f"✅ 解包完成：{count} 个文件 -> {output_dir}")
    return count


def add_files(
    lica_path: str, files: Dict[str, Union[bytes, str]], overwrite: bool = True
) -> int:
    """
    向 lica 文件中添加或更新文件。

    :param lica_path: lica 文件路径
    :param files: 字典，键为相对路径，值为文件内容（bytes 或 Base64 字符串）
    :param overwrite: 如果键已存在，是否覆盖；若为 False 且键存在，则跳过
    :return: 实际添加/更新的文件数量
    """
    data = _load_lica(lica_path)
    added = 0

    for rel_path, content in files.items():
        if not overwrite and rel_path in data:
            continue

        if isinstance(content, bytes):
            b64_str = base64.b64encode(content).decode("utf-8")
        elif isinstance(content, str):
            b64_str = content  # 假设已是 Base64
        else:
            raise TypeError(
                f"文件内容必须是 bytes 或 Base64 字符串，得到 {type(content)}"
            )

        data[rel_path] = b64_str
        added += 1

    if added > 0:
        _save_lica(lica_path, data)
    return added


def add_files_from_paths(lica_path, file_paths, base_dir=None, overwrite=True):
    """
    通过文件路径列表向 lica 文件添加文件。
    :param file_paths: 文件路径列表，或字典 {相对路径: 绝对路径}
    :param base_dir: 如果传入列表，则以此为基础计算相对路径；如果传入字典，则忽略 base_dir
    """
    files_dict = {}

    if isinstance(file_paths, dict):
        # 直接使用提供的映射
        for rel_path, abs_path in file_paths.items():
            with open(abs_path, "rb") as f:
                files_dict[rel_path] = f.read()
    else:
        # 列表模式：使用 base_dir 计算相对路径
        for abs_path in file_paths:
            if base_dir:
                rel_path = os.path.relpath(abs_path, base_dir).replace(os.sep, "/")
            else:
                rel_path = os.path.basename(abs_path)
            with open(abs_path, "rb") as f:
                files_dict[rel_path] = f.read()

    return add_files(lica_path, files_dict, overwrite)


def remove_files(lica_path: str, files: Union[str, List[str]]) -> int:
    """
    从 lica 文件中移除指定文件。

    :param lica_path: lica 文件路径
    :param files: 要移除的相对路径（字符串）或路径列表
    :return: 实际移除的文件数量
    """
    if isinstance(files, str):
        files = [files]

    data = _load_lica(lica_path)
    removed = 0

    for rel_path in files:
        if rel_path in data:
            del data[rel_path]
            removed += 1

    if removed > 0:
        _save_lica(lica_path, data)
    return removed
