import sys
import subprocess
import pkg_resources
from logger import print_log

def install_required_packages():
    """必要なパッケージをインストールする"""
    required_packages = {
        'discord.py': 'discord.py',
        'python-dotenv': 'python-dotenv'
    }

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [pkg for pkg, pip_name in required_packages.items() if pkg not in installed_packages]

    if missing_packages:
        print_log("必要なパッケージのインストールを開始します...", "SETUP")
        for pkg in missing_packages:
            print_log(f"パッケージ '{pkg}' をインストール中...", "INSTALL")
            try:
                # pipの出力を非表示にする
                subprocess.check_call(
                    [sys.executable, '-m', 'pip', 'install', required_packages[pkg]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print_log(f"パッケージ '{pkg}' のインストールが完了しました", "SUCCESS")
            except subprocess.CalledProcessError:
                print_log(f"パッケージ '{pkg}' のインストールに失敗しました", "ERROR")
        print_log("すべてのパッケージのインストールが完了しました", "SETUP")
    else:
        print_log("必要なパッケージはすべてインストール済みです", "SETUP")

if __name__ == '__main__':
    install_required_packages()