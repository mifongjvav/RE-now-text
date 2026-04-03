# ===== 用户可修改的配置 =====
$rootDir = "./level"
$outputFile = "./build_package.py"
$resDir = "./res"
# ============================

python -c @"
import lica
lica.pack_directory('res.lica', '$resDir')
print('资源打包完成！')
"@

$rootFull = Resolve-Path -Path $rootDir -ErrorAction Stop
$rootName = Split-Path -Leaf $rootFull
$isCurrentDir = ($rootFull.Path -eq (Get-Location).Path)

if (Test-Path $outputFile) { Remove-Item $outputFile -Force }

$files = Get-ChildItem -Path $rootFull -Recurse -Filter *.py | Where-Object {
    $_.Name -ne '__init__.py' -and $_.FullName -ne (Resolve-Path $outputFile -ErrorAction SilentlyContinue)
}

function Get-RelativePath {
    param([string]$base, [string]$target)
    $base = $base.TrimEnd('\')
    $target = $target.TrimEnd('\')
    if ($target -like "$base*") {
        return $target.Substring($base.Length).TrimStart('\')
    }
    return $target
}

# 收集所有 import 语句（每个作为单独字符串）
$importLines = foreach ($file in $files) {
    $relativePath = Get-RelativePath -base $rootFull.Path -target $file.FullName
    $relativeModule = $relativePath -replace '\.py$', '' -replace '[\\/]', '.'

    if ($isCurrentDir) {
        $module = $relativeModule
    } else {
        $safeRootName = $rootName -replace '[^a-zA-Z0-9_]', '_'
        $module = "$safeRootName.$relativeModule"
    }
    # 返回带缩进的 import 语句
    "    import $module  # noqa: F401"
}

# 用换行符连接所有 import 语句
$importsText = $importLines -join "`n"

# 构建完整的 Python 代码块（添加 import time）
$codeBlock = @"
import time

if time.time() == 1:  # 骗过 pyinstaller 的静态分析，确保打包所有关卡模块且不执行
$importsText
"@

Set-Content -Path $outputFile -Value $codeBlock -Encoding UTF8
Write-Host "Generated import statements to $outputFile (scanning root: $rootFull)"

$pyArgs = @(
    '--console',
    '--add-data', 'MenuLite\Menu\MlConfig.yaml;Menu',
    '--add-data', 'res.lica;.',
    '--name', 'RE-now-text',
    'Main.py'
)
# pyinstaller @pyArgs