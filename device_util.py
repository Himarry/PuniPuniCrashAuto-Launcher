from adbutils import adb
import time
import cv2

def get_device():
    return adb.device()

def get_screenshot(device, save_path='screenshot.png'):
    device.shell('screencap -p /sdcard/screenshot.png')
    device.sync.pull('/sdcard/screenshot.png', save_path)
    # 画像を読み込んでnumpy配列として返す
    img = cv2.imread(save_path, 0)  # グレースケールで読み込み
    if img is None:
        print(f'[警告] スクリーンショットの読み込みに失敗: {save_path}')
    return img

def tap(device, pos):
    x, y = pos
    device.shell(f'input tap {x} {y}')

def swipe(device, start, end, duration=500):
    x1, y1 = start
    x2, y2 = end
    device.shell(f'input swipe {x1} {y1} {x2} {y2} {duration}')
