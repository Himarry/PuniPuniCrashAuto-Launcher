from 参考用.config import TARGET_APP_PACKAGE, MAIN_ACTIVITY
import time

def launch_app(device):
    print('アプリ起動コマンド送信')
    try:
        device.shell(f'am start -n {TARGET_APP_PACKAGE}/{MAIN_ACTIVITY}')
        time.sleep(5)
    except Exception as e:
        print(f'アプリ起動失敗: {e}')
