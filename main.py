import time
from adbutils import adb
from crash_recovery import crash_recovery
from image_util import load_template, find_image_on_screen
from device_util import get_screenshot, tap
import threading
import subprocess

PORTS = [5725, 5735, 5695]

def adb_connect_all():
    for port in PORTS:
        serial = f'127.0.0.1:{port}'
        try:
            result = subprocess.run(['adb', 'connect', serial], capture_output=True, text=True)
            print(result.stdout.strip())
        except Exception as e:
            print(f'adb connect {serial} 失敗: {e}')

def is_app_running(device, package_name):
    """Check if the app is running on the device."""
    try:
        output = device.shell(f'pm list packages | grep {package_name}')
        return bool(output.strip())
    except Exception as e:
        print(f'アプリの状態を確認中にエラーが発生しました: {e}')
        return False

def device_worker(port):
    serial = f'127.0.0.1:{port}'
    home_img = load_template('home.png')
    google_play_img = load_template('google_play.png')
    google_login_img = load_template('google_login.png')
    gmail_img = load_template('gmail.png')
    play_img = load_template('play.png')
    result_next_img = load_template('result_next.png')
    # 新しい監視対象画像
    back_img = load_template('back.png')
    score_1_img = load_template('score_1.png')
    score_redJ_img = load_template('score_redJ.png')
    ranking_img = load_template('ranking.png')
    koukan_1_img = load_template('koukan_1.png')
    koukan_2_img = load_template('koukan_2.png')
    # タップ対象画像
    box_key_list_close_img = load_template('box-key_list_close.png')
    score_close_img = load_template('score_close.png')
    while True:
        try:
            # エミュレーターが起動していない場合は何も出力せずスキップ
            if serial not in [d.serial for d in adb.device_list()]:
                time.sleep(5)
                continue
            device = adb.device(serial=serial)
            # アプリが起動していない場合もスキップ
            if not is_app_running(device, 'com.Level5.YWP'):
                time.sleep(5)
                continue
            screenshot = get_screenshot(device)
            
            # play.pngが検出されたら検出されなくなるまで連打
            play_pos = find_image_on_screen(play_img, screenshot, threshold=0.7)
            if play_pos:
                print(f'play.png検出→連打開始 ({serial})')
                while True:
                    screenshot = get_screenshot(device)
                    play_pos = find_image_on_screen(play_img, screenshot, threshold=0.7)
                    if play_pos:
                        print(f'play.png連打中→タップ ({serial})')
                        tap(device, play_pos)
                    else:
                        print(f'play.png検出されなくなりました→連打終了 ({serial})')
                        break
                continue  # play処理完了後は次のループへ
            
            # result_next.pngが検出されたら検出されなくなるまで連打
            result_next_pos = find_image_on_screen(result_next_img, screenshot, threshold=0.7)
            if result_next_pos:
                print(f'result_next.png検出→連打開始 ({serial})')
                while True:
                    screenshot = get_screenshot(device)
                    result_next_pos = find_image_on_screen(result_next_img, screenshot, threshold=0.7)
                    if result_next_pos:
                        print(f'result_next.png連打中→タップ ({serial})')
                        tap(device, result_next_pos)
                    else:
                        print(f'result_next.png検出されなくなりました→連打終了 ({serial})')
                        break
                continue  # result_next処理完了後は次のループへ
            
            # 新しい監視・タップ処理
            # ①back.pngを検知したらタップ
            back_pos = find_image_on_screen(back_img, screenshot, threshold=0.8)
            if back_pos:
                print(f'back.png検出→タップ ({serial})')
                tap(device, back_pos)
                continue
            
            # ②score_1.pngを検知したらbox-key_list_close.pngをタップ
            score_1_pos = find_image_on_screen(score_1_img, screenshot, threshold=0.8)
            if score_1_pos:
                box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
                if box_key_close_pos:
                    print(f'score_1.png検出→box-key_list_close.pngタップ ({serial})')
                    tap(device, box_key_close_pos)
                else:
                    print(f'score_1.png検出したがbox-key_list_close.png見つからず ({serial})')
                continue
            
            # ③score_redJ.pngを検知したらscore_close.pngをタップ
            score_redJ_pos = find_image_on_screen(score_redJ_img, screenshot, threshold=0.8)
            if score_redJ_pos:
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.8)
                if score_close_pos:
                    print(f'score_redJ.png検出→score_close.pngタップ ({serial})')
                    tap(device, score_close_pos)
                else:
                    print(f'score_redJ.png検出したがscore_close.png見つからず ({serial})')
                continue
            
            # ④ranking.pngを検知したらscore_close.pngをタップ
            ranking_pos = find_image_on_screen(ranking_img, screenshot, threshold=0.8)
            if ranking_pos:
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.8)
                if score_close_pos:
                    print(f'ranking.png検出→score_close.pngタップ ({serial})')
                    tap(device, score_close_pos)
                else:
                    print(f'ranking.png検出したがscore_close.png見つからず ({serial})')
                continue
            
            # ⑤koukan_1.pngを検知したらkoukan_1.png自体をタップ
            koukan_1_pos = find_image_on_screen(koukan_1_img, screenshot, threshold=0.8)
            if koukan_1_pos:
                print(f'koukan_1.png検出→koukan_1.pngタップ ({serial})')
                tap(device, koukan_1_pos)
                continue
            
            # ⑥koukan_2.pngを検知したらscore_close.pngをタップ
            koukan_2_pos = find_image_on_screen(koukan_2_img, screenshot, threshold=0.8)
            if koukan_2_pos:
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.8)
                if score_close_pos:
                    print(f'koukan_2.png検出→score_close.pngタップ ({serial})')
                    tap(device, score_close_pos)
                else:
                    print(f'koukan_2.png検出したがscore_close.png見つからず ({serial})')
                continue
            
            # home.png/google_play.png/google_login.png/gmail.pngが出ていたらクラッシュ復旧
            home_pos = find_image_on_screen(home_img, screenshot, threshold=0.8)
            google_play_pos = find_image_on_screen(google_play_img, screenshot, threshold=0.8)
            google_login_pos = find_image_on_screen(google_login_img, screenshot, threshold=0.8)
            gmail_pos = find_image_on_screen(gmail_img, screenshot, threshold=0.8)
            if home_pos or google_play_pos or google_login_pos or gmail_pos:
                print(f'クラッシュ復帰処理を実行します... ({serial})')
                crash_recovery(device)
        except Exception as e:
            print(f'デバイス {serial} でエラー: {e}')
        time.sleep(5)

def main():
    print('クラッシュ復帰専用スクリプト 起動')
    adb_connect_all()
    threads = []
    for port in PORTS:
        t = threading.Thread(target=device_worker, args=(port,), daemon=True)
        t.start()
        threads.append(t)
    # メインスレッドを維持
    while True:
        time.sleep(60)

if __name__ == '__main__':
    main()
