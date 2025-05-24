from datetime import datetime

# ANSIカラーコード
COLORS = {
    "STARTUP": "\033[95m",  # マゼンタ
    "SETUP": "\033[96m",    # シアン
    "INSTALL": "\033[93m",  # イエロー
    "SUCCESS": "\033[92m",  # グリーン
    "ERROR": "\033[91m",    # レッド
    "WARNING": "\033[93m",  # イエロー
    "BOT": "\033[94m",      # ブルー
    "CONFIG": "\033[95m",   # マゼンタ
    "COMMANDS": "\033[96m", # シアン
    "COMMAND": "\033[92m",  # グリーン
    "TRIGGERS": "\033[96m", # シアン
    "TRIGGER": "\033[92m",  # グリーン
    "RESPONSE": "\033[93m", # イエロー
    "WELCOME": "\033[95m",  # マゼンタ
    "INFO": "\033[97m",     # ホワイト
    "RESET": "\033[0m"      # リセット
}

def print_log(message, type="INFO"):
    """ログメッセージを整形して出力"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = COLORS.get(type, COLORS["INFO"])
    print(f"\033[90m{timestamp}\033[0m [{color}{type}{COLORS['RESET']}] {message}") 