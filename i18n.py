import os
import sys
import yaml
from i18n_core import get_system_locale


def _expand_flat_keys(flat_dict: dict) -> dict:
    result = {}

    for key, value in flat_dict.items():
        parts = key.split(".")
        cur = result

        for part in parts[:-1]:
            if part not in cur or not isinstance(cur[part], dict):
                cur[part] = {}
            cur = cur[part]

        cur[parts[-1]] = value

    return result


def _load_yaml_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return {}

        return _expand_flat_keys(data)


class LangNode:
    __slots__ = ("_primary", "_fallback", "_path")

    def __init__(self, primary: dict, fallback: dict, path=""):
        self._primary = primary or {}
        self._fallback = fallback or {}
        self._path = path

    def _get_value(self, key):
        if key in self._primary:
            fb = self._fallback.get(key) if isinstance(self._fallback, dict) else None
            return self._primary[key], fb

        if key in self._fallback:
            return self._fallback[key], None

        return None, None

    def __getattr__(self, name: str):
        value, fallback_value = self._get_value(name)
        new_path = f"{self._path}.{name}" if self._path else name

        if value is None:
            return LangNode({}, {}, new_path)

        if isinstance(value, dict):
            return LangNode(
                value,
                fallback_value if isinstance(fallback_value, dict) else {},
                new_path,
            )

        return LangNode({"__value__": value}, {}, new_path)

    def __getitem__(self, name: str):
        return self.__getattr__(name)

    def _resolve(self):
        if "__value__" in self._primary:
            return self._primary["__value__"]

        if "__value__" in self._fallback:
            return self._fallback["__value__"]

        return self._path

    def __str__(self):
        return str(self._resolve())

    def __repr__(self):
        return f"<LangNode path='{self._path}' value={self._resolve()!r}>"

    def __iter__(self):
        return iter(str(self))

    def __len__(self):
        return len(str(self))

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __contains__(self, item):
        return item in str(self)

    def get(self, dotted_path: str, default=None):
        cur = self
        for part in dotted_path.split("."):
            cur = getattr(cur, part)

        result = cur._resolve()
        return result if result is not None else default

    def __call__(self, dotted_path: str, default=None, **kwargs):
        value = self.get(dotted_path, default)

        if isinstance(value, str) and kwargs:
            try:
                return value.format(**kwargs)
            except Exception:
                return value

        return value


def init_lang(default_lang: str = "en_US"):
    lang_dir = os.path.join(os.path.dirname(__file__), "lang")

    if not os.path.isdir(lang_dir):
        raise FileNotFoundError(f"语言目录不存在：{lang_dir}")

    langs = {}

    for filename in os.listdir(lang_dir):
        if filename.endswith((".yaml", ".yml")):
            code = os.path.splitext(filename)[0]
            langs[code] = _load_yaml_file(os.path.join(lang_dir, filename))

    if not langs:
        raise RuntimeError("没有任何语言文件")

    current_locale = get_system_locale() or default_lang
    current_locale = current_locale.split(".")[0]

    primary = langs.get(current_locale, {})
    fallback = langs.get(default_lang, {})

    sys.lang = LangNode(primary, fallback)
    return sys.lang
