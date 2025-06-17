import time
from image_util import load_template, find_image_on_screen
from device_util import get_screenshot, tap, swipe
from app_control import launch_app
from adbutils import adb

# 座標指定（仮: 必要に応じて調整）
LOGIN_POS = (370, 690)
LOGIN_OK_POS = (480, 720)
TITLE_POS = (360, 600)
ACCOUNT_POS = (360, 800)
USER_OK_POS = (650, 1200)
SCROLL_START = (345, 1030) 
SCROLL_END = (345, 107)

PORTS = [5725, 5735, 5695]

def crash_recovery_single(dev):
    serial = dev.serial
    try:
        port = int(serial.split(':')[-1]) if ':' in serial else None
    except Exception:
        port = None
    port_to_account_img = {
        5725: load_template('account_1.png'),
        5735: load_template('account_3.png'),
        5695: load_template('account_2.png'),
    }
    stop_img = load_template('click_stop.png')
    screenshot = get_screenshot(dev)
    otokuri_start_img = load_template('click_start.png')
    is_otokuri_start = find_image_on_screen(otokuri_start_img, screenshot, threshold=0.8) is not None
    pos = find_image_on_screen(stop_img, screenshot, threshold=0.8)
    if pos and not is_otokuri_start:
        print(f'オトクリ停止ボタン(click_stop_result.png)→タップ')
        tap(dev, pos)
        time.sleep(2)
    elif is_otokuri_start:
        print('オトクリスタートボタンが表示されているため停止ボタンは押しません')
    launch_app(dev)
    wait_and_tap(dev, load_template('login.png'), 'ログインボタン', pos=LOGIN_POS, threshold=0.5)
    time.sleep(2)
    print('ログインボタン(2回目)→タップ')
    tap(dev, LOGIN_POS)
    time.sleep(1)
    wait_and_tap(dev, load_template('login_ok.png'), 'ログイン確認', pos=LOGIN_OK_POS)
    wait_and_tap(dev, None, 'タイトル画面', pos=TITLE_POS)
    account_img = port_to_account_img.get(port)
    wait_and_tap(dev, account_img, f'アカウント選択({port})')
    wait_and_tap(dev, None, '決定', pos=USER_OK_POS)
    screenshot = get_screenshot(dev)
    if find_image_on_screen(load_template('notice.png'), screenshot, threshold=0.9):
        print('notice.png検出→ボックスリスト閉じるボタンをタップ')
        box_close_img = load_template('box-key_list_close.png')
        box_close_pos = find_image_on_screen(box_close_img, screenshot, threshold=0.9)
        if box_close_pos:
            tap(dev, box_close_pos)
            time.sleep(1)
    # スタンプカード処理
    screenshot = get_screenshot(dev)
    stamp1_img = load_template('stamp_crad_1.png')
    stamp2_img = load_template('stamp_crad_2.png')
    stamp_ok_img = load_template('stamp_crad_ok.png')
    stamp1_pos = find_image_on_screen(stamp1_img, screenshot, threshold=0.9)
    if stamp1_pos:
        print('stamp_crad_1検出→OKタップ')
        ok_pos = find_image_on_screen(stamp_ok_img, screenshot, threshold=0.9)
        if ok_pos:
            tap(dev, ok_pos)
            time.sleep(1)
    screenshot = get_screenshot(dev)
    stamp2_pos = find_image_on_screen(stamp2_img, screenshot, threshold=0.9)
    if stamp2_pos:
        print('stamp_crad_2検出→OKタップ')
        ok_pos = find_image_on_screen(stamp_ok_img, screenshot, threshold=0.9)
        if ok_pos:
            tap(dev, ok_pos)
            time.sleep(1)
    print('スクロール')
    swipe(dev, SCROLL_START, SCROLL_END)
    time.sleep(2)
    wait_and_tap(dev, None, 'ステージ選択', pos=(360, 600))
    time.sleep(2)

# クラッシュ復旧処理（複数デバイス対応）
def crash_recovery(device=None):
    print('クラッシュ検知: 復旧処理開始')
    devices = [adb.device(serial=f'127.0.0.1:{port}') for port in PORTS] if device is None else [device]
    for dev in devices:
        crash_recovery_single(dev)

def wait_and_tap(dev, template, desc, pos=None, threshold=0.8, timeout=60, interval=2):
    """指定画像が検出されるまで待機し、検出後タップする"""
    start = time.time()
    while True:
        screenshot = get_screenshot(dev)
        found = None
        if template is not None:
            # Noneでなければ画像認識
            found = find_image_on_screen(template, screenshot, threshold=threshold)
        elif pos is not None:
            found = pos
        if found is not None:
            print(f'{desc}→タップ')
            tap(dev, found)
            time.sleep(2)
            break
        if time.time() - start > timeout:
            print(f'{desc}が{timeout}秒以内に検出できませんでした')
            break
        time.sleep(interval)
