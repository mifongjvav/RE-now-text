import time

if time.time() == 1:  # 骗过 pyinstaller 的静态分析，确保打包所有关卡模块且不执行
    import level.init  # noqa: F401
    import level.l3lib  # noqa: F401
    import level.l4lib  # noqa: F401
    import level.level1  # noqa: F401
    import level.level2  # noqa: F401
    import level.level3  # noqa: F401
    import level.level4  # noqa: F401
