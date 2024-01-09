# build.py
import os
import shutil
import subprocess


def build_executable():
    # 执行 PyInstaller 命令
    pyinstaller_cmd = ('pyinstaller '
                       '--onefile  '
                       '--strip '
                       '--noconsole '
                       '--add-data "Mandarin.dat;xpinyin" '
                       '--upx-dir=upx.exe '
                       'main.py')
    subprocess.run(pyinstaller_cmd, shell=True)
    # 将static目录复制到dist目录
    source_static = 'static'
    destination_static = os.path.join('dist', 'static')
    try:
        shutil.rmtree(destination_static)
    except FileNotFoundError:
        pass
    shutil.copytree(source_static, destination_static)


if __name__ == '__main__':
    build_executable()
