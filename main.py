import time
from device_util import get_device
from crash_recovery import crash_recovery

def main():
    print('クラッシュ復帰専用スクリプト 起動')
    device = get_device()
    while True:
        print('クラッシュ復帰処理を実行します...')
        crash_recovery(device)
        time.sleep(5)

if __name__ == '__main__':
    main()
