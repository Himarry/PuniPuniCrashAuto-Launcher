import time
import threading
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
    # home.pngまたはgoogle_play.pngまたはgoogle_login.pngまたはgmail.pngが出ていたら必ず強制終了→起動し、そのままログイン処理も必ず実行
    screenshot = get_screenshot(dev)
    home_img = load_template('home.png')
    google_play_img = load_template('google_play.png')
    google_login_img = load_template('google_login.png')
    gmail_img = load_template('gmail.png')
    home_pos = find_image_on_screen(home_img, screenshot, threshold=0.8)
    google_play_pos = find_image_on_screen(google_play_img, screenshot, threshold=0.8)
    google_login_pos = find_image_on_screen(google_login_img, screenshot, threshold=0.8)
    gmail_pos = find_image_on_screen(gmail_img, screenshot, threshold=0.8)
    if home_pos or google_play_pos or google_login_pos or gmail_pos:
        print('home.png/google_play.png/google_login.png/gmail.png検出→オトクリ停止→アプリ強制終了→再起動→画面タップ→ログイン処理')
        # 再起動前にオトクリ停止ボタンをタップ
        stop_img = load_template('click_stop.png')
        screenshot = get_screenshot(dev)
        stop_pos = find_image_on_screen(stop_img, screenshot, threshold=0.8)
        if stop_pos:
            print('再起動前→オトクリ停止ボタンタップ')
            tap(dev, stop_pos)
            time.sleep(2)
        try:
            dev.shell(f'am force-stop com.Level5.YWP')
            time.sleep(2)
        except Exception as e:
            print(f'アプリ強制終了失敗: {e}')
        launch_app(dev)
        # アプリ起動直後に画面中央を1回タップ
        time.sleep(3)  # 起動直後の画面安定待ち
        tap(dev, (360, 800))  # 画面中央付近（座標は必要に応じて調整）
        time.sleep(1)
        # ここからログイン処理
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
        print('[デバッグ] 決定完了→オトクリ開始待機開始')
        click_start_img = load_template('click_start.png')
        wait_and_tap(dev, click_start_img, 'オトクリ開始', threshold=0.8, timeout=30, interval=2)
        print('[デバッグ] 復旧処理完了→return')
        return  # 復旧処理完了後はここで終了
    
    print('[デバッグ] 停止ボタン判定ブロックに到達')
    stop_img = load_template('click_stop.png')
    screenshot = get_screenshot(dev)
    otokuri_start_img = load_template('click_start.png')
    is_otokuri_start = find_image_on_screen(otokuri_start_img, screenshot, threshold=0.8) is not None
    pos = find_image_on_screen(stop_img, screenshot, threshold=0.8)
    print(f'[デバッグ] 停止ボタン: 検出座標={pos}, threshold=0.8')
    print(f'[デバッグ] オトクリスタートボタン: 検出={is_otokuri_start}')
    if pos and not is_otokuri_start:
        print(f'オトクリ停止ボタン(click_stop_result.png)→タップ')
        tap(dev, pos)
        time.sleep(2)
    elif is_otokuri_start:
        print('オトクリスタートボタンが表示されているため停止ボタンは押しません')
    launch_app(dev)
    time.sleep(2)
    screenshot = get_screenshot(dev)
    # ここから必ずログイン処理
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
    # 決定ボタン押下後、error_1.pngが表示されたらerror_2.pngを最大5回タップ
    for _ in range(5):
        screenshot = get_screenshot(dev)
        error1_img = load_template('error_1.png')
        error2_img = load_template('error_2.png')
        error1_pos = find_image_on_screen(error1_img, screenshot, threshold=0.9)
        if error1_pos:
            print('error_1.png検出→error_2.pngをタップ')
            error2_pos = find_image_on_screen(error2_img, screenshot, threshold=0.9)
            if error2_pos:
                tap(dev, error2_pos)
                time.sleep(1)
        else:
            break
    # notice.png検出時の処理を最大5回まで繰り返す
    for _ in range(5):
        screenshot = get_screenshot(dev)
        if find_image_on_screen(load_template('notice.png'), screenshot, threshold=0.9):
            print('notice.png検出→ボックスリスト閉じるボタンをタップ')
            box_close_img = load_template('box-key_list_close.png')
            box_close_pos = find_image_on_screen(box_close_img, screenshot, threshold=0.9)
            if box_close_pos:
                tap(dev, box_close_pos)
                time.sleep(1)
        else:
            break
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
    time.sleep(2)
    click_start_img = load_template('click_start.png')
    # オトクリ開始ボタンが出ていれば必ずタップ（検出できるまで待つ）
    wait_and_tap(dev, click_start_img, 'オトクリ開始', threshold=0.8, timeout=300, interval=2)

# クラッシュ復旧処理（複数デバイス対応）
def crash_recovery(device=None):
    print('クラッシュ検知: 復旧処理開始')
    devices = [adb.device(serial=f'127.0.0.1:{port}') for port in PORTS] if device is None else [device]
    for dev in devices:
        crash_recovery_single(dev)

def wait_and_tap(dev, template, desc, pos=None, threshold=0.8, timeout=60, interval=2):
    """指定画像が検出されるまで待機し、検出後タップする（デバッグ出力付き）"""
    start = time.time()
    while True:
        screenshot = get_screenshot(dev)
        found = None
        if template is not None:
            found = find_image_on_screen(template, screenshot, threshold=threshold)
            print(f'[デバッグ] {desc}: 検出座標={found}, threshold={threshold}')
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

def error_monitor_thread(dev):
    error1_img = load_template('error_1.png')
    error2_img = load_template('error_2.png')
    while True:
        try:
            screenshot = get_screenshot(dev)
            error1_pos = find_image_on_screen(error1_img, screenshot, threshold=0.9)
            if error1_pos:
                print('error_1.png検出→error_2.pngをタップ')
                error2_pos = find_image_on_screen(error2_img, screenshot, threshold=0.9)
                if error2_pos:
                    tap(dev, error2_pos)
                    time.sleep(1)
        except Exception as e:
            print(f'エラーモニタで例外: {e}')
        time.sleep(2)

def is_app_running(dev, package_name):
    try:
        # 実行中のアクティビティ取得
        result = dev.shell(f'dumpsys activity activities | grep mResumedActivity')
        return package_name in result
    except Exception as e:
        print(f'アプリ起動判定エラー: {e}')
        return False
