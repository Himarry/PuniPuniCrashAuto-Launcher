import time
from adbutils import adb
from crash_recovery import crash_recovery
from image_util import load_template, find_image_on_screen
from device_util import get_screenshot, tap
import threading
import subprocess
from datetime import datetime

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

def safe_tap(device, tap_pos, team_3_pos, serial, action_name):
    """team_3.pngとの重複をチェックしてからタップする安全な関数"""
    if team_3_pos and tap_pos:
        # 座標の距離をチェック（50ピクセル以内なら重複とみなす）
        distance = ((tap_pos[0] - team_3_pos[0])**2 + (tap_pos[1] - team_3_pos[1])**2)**0.5
        if distance < 50:
            print(f'{action_name}タップ位置がteam_3.pngと重複のためタップ無効化 ({serial})')
            return False
    
    tap(device, tap_pos)
    return True

def device_worker(port):
    serial = f'127.0.0.1:{port}'
    # フレームレート計測用変数
    last_time = time.time()
    frame_count = 0
    fps_display_interval = 30  # 30フレームごとにFPSを表示
    
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
    team_img = load_template('team.png')
    score_item_img = load_template('score_item.png')
    team_yokai_img = load_template('team_yokai.png')
    whisper_img = load_template('whisper.png')
    ranking_2_img = load_template('ranking_2.png')
    yubin_img = load_template('yubin.png')
    score_atk_img = load_template('score_atk.png')
    team_3_img = load_template('team_3.png')
    takara_img = load_template('takara.png')
    key_img = load_template('key.png')
    # タップ対象画像
    box_key_list_close_img = load_template('box-key_list_close.png')
    score_close_img = load_template('score_close.png')
    while True:
        try:
            # エミュレーターが起動していない場合は何も出力せずスキップ
            if serial not in [d.serial for d in adb.device_list()]:
                time.sleep(0.5)  # デバイス未接続時のみ少し長めの待機
                continue
            device = adb.device(serial=serial)
            # アプリが起動していない場合もスキップ
            if not is_app_running(device, 'com.Level5.YWP'):
                time.sleep(0.5)  # アプリ未起動時のみ少し長めの待機
                continue
            screenshot = get_screenshot(device)
            
            # score_atk.pngが検知された場合はscore_close.pngとwhisper.png以外の操作を無効化
            score_atk_pos = find_image_on_screen(score_atk_img, screenshot, threshold=0.8)
            # team_3.pngの誤検知防止用チェック
            team_3_pos = find_image_on_screen(team_3_img, screenshot, threshold=0.8)
            
            if score_atk_pos:
                print(f'score_atk.png検出 → score_close.pngとwhisper.png以外の操作無効化 ({serial})')
                # score_close.pngをチェックしてタップ
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.8)
                if score_close_pos:
                    print(f'score_atk.png画面でscore_close.png検出→タップ ({serial})')
                    tap(device, score_close_pos)
                    continue
                # whisper.pngをチェックしてタップ
                whisper_pos = find_image_on_screen(whisper_img, screenshot, threshold=0.8)
                if whisper_pos:
                    print(f'score_atk.png画面でwhisper.png検出→タップ ({serial})')
                    tap(device, whisper_pos)
                    continue
                continue
            
            # フレームレート計測とリアルタイム表示
            frame_count += 1
            current_time = time.time()
            if frame_count % fps_display_interval == 0:
                elapsed_time = current_time - last_time
                fps = fps_display_interval / elapsed_time
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f'[{timestamp}] スクショ撮影中 - FPS: {fps:.1f} ({serial})')
                last_time = current_time
            
            # takara.pngが検知されている場合はbox-key_list_close.png以外タップ禁止
            takara_pos = find_image_on_screen(takara_img, screenshot, threshold=0.8)
            if takara_pos:
                box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
                if box_key_close_pos:
                    print(f'takara.png検出→box-key_list_close.pngタップ ({serial})')
                    safe_tap(device, box_key_close_pos, team_3_pos, serial, 'box-key_list_close.png')
                else:
                    print(f'takara.png検出中→box-key_list_close.png以外タップ禁止 ({serial})')
                continue
            
            # key.pngが検知されている場合はbox-key_list_close.png以外タップ禁止
            key_pos = find_image_on_screen(key_img, screenshot, threshold=0.8)
            if key_pos:
                box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
                if box_key_close_pos:
                    print(f'key.png検出→box-key_list_close.pngタップ ({serial})')
                    safe_tap(device, box_key_close_pos, team_3_pos, serial, 'box-key_list_close.png')
                else:
                    print(f'key.png検出中→box-key_list_close.png以外タップ禁止 ({serial})')
                continue
            
            # score_redJ.pngとplay.pngの両方が同時に検知されたらscore_close.pngをタップ
            score_redJ_pos = find_image_on_screen(score_redJ_img, screenshot, threshold=0.8)
            play_pos = find_image_on_screen(play_img, screenshot, threshold=0.7)
            if score_redJ_pos and play_pos:
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.8)
                if score_close_pos:
                    print(f'score_redJ.pngとplay.png同時検出→score_close.pngタップ ({serial})')
                    safe_tap(device, score_close_pos, team_3_pos, serial, 'score_close.png')
                else:
                    print(f'score_redJ.pngとplay.png同時検出したがscore_close.png見つからず ({serial})')
                continue
            
            # team.pngとplay.pngの両方が同時に検知されたらbox-key_list_close.pngをタップ
            team_pos = find_image_on_screen(team_img, screenshot, threshold=0.8)
            if team_pos and play_pos:
                box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
                if box_key_close_pos:
                    print(f'team.pngとplay.png同時検出→box-key_list_close.pngタップ ({serial})')
                    safe_tap(device, box_key_close_pos, team_3_pos, serial, 'box-key_list_close.png')
                else:
                    print(f'team.pngとplay.png同時検出したがbox-key_list_close.png見つからず ({serial})')
                continue
            
            # whisper.pngとranking_2.pngの両方が同時に検知されたらwhisper.pngをタップ
            whisper_pos = find_image_on_screen(whisper_img, screenshot, threshold=0.8)
            ranking_2_pos = find_image_on_screen(ranking_2_img, screenshot, threshold=0.8)
            if whisper_pos and ranking_2_pos:
                print(f'whisper.pngとranking_2.png同時検出→whisper.pngタップ ({serial})')
                safe_tap(device, whisper_pos, team_3_pos, serial, 'whisper.png')
                continue
            
            # play.pngが検出されたら検出されなくなるまで連打
            play_pos = find_image_on_screen(play_img, screenshot, threshold=0.7)
            if play_pos:
                # play.pngタップの抑制条件をチェック
                score_item_pos = find_image_on_screen(score_item_img, screenshot, threshold=0.8)
                team_yokai_pos = find_image_on_screen(team_yokai_img, screenshot, threshold=0.8)
                score_redJ_pos = find_image_on_screen(score_redJ_img, screenshot, threshold=0.8)
                team_pos = find_image_on_screen(team_img, screenshot, threshold=0.8)
                
                # 抑制条件の判定
                suppress_play = False
                if score_item_pos and team_yokai_pos:
                    print(f'score_item.png + team_yokai.png検出中 → play.pngタップ抑制 ({serial})')
                    suppress_play = True
                elif score_item_pos and score_redJ_pos:
                    print(f'score_item.png + score_redJ.png検出中 → play.pngタップ抑制 ({serial})')
                    suppress_play = True
                elif score_item_pos and team_pos:
                    print(f'score_item.png + team.png検出中 → play.pngタップ抑制 ({serial})')
                    suppress_play = True
                elif score_redJ_pos:
                    print(f'score_redJ.png検出中 → play.pngタップ抑制 ({serial})')
                    suppress_play = True
                
                if not suppress_play:
                    print(f'play.png検出→連打開始 ({serial})')
                    while True:
                        screenshot = get_screenshot(device)
                        play_pos = find_image_on_screen(play_img, screenshot, threshold=0.7)
                        if play_pos:
                            # 連打中も抑制条件を再チェック
                            score_item_pos = find_image_on_screen(score_item_img, screenshot, threshold=0.8)
                            team_yokai_pos = find_image_on_screen(team_yokai_img, screenshot, threshold=0.8)
                            score_redJ_pos = find_image_on_screen(score_redJ_img, screenshot, threshold=0.8)
                            team_pos = find_image_on_screen(team_img, screenshot, threshold=0.8)
                            
                            # 連打中の抑制条件チェック
                            if (score_item_pos and team_yokai_pos) or \
                               (score_item_pos and score_redJ_pos) or \
                               (score_item_pos and team_pos) or \
                               score_redJ_pos:
                                print(f'連打中に抑制条件検出 → 連打停止 ({serial})')
                                break
                            
                            print(f'play.png連打中→タップ ({serial})')
                            tap(device, play_pos)
                        else:
                            print(f'play.png検出されなくなりました→連打終了 ({serial})')
                            break
                continue  # play処理完了後は次のループへ
            
            # result_next.pngが検出されたら検出されなくなるまで連打
            # ただし、box-key_list_close.pngが表示されている場合は検知しない
            box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
            if not box_key_close_pos:
                result_next_pos = find_image_on_screen(result_next_img, screenshot, threshold=0.85)
                if result_next_pos:
                    print(f'result_next.png検出→連打開始 ({serial})')
                    while True:
                        screenshot = get_screenshot(device)
                        # 連打中もbox-key_list_close.pngをチェック
                        box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
                        if box_key_close_pos:
                            print(f'連打中にbox-key_list_close.png検出 → 連打停止 ({serial})')
                            break
                        result_next_pos = find_image_on_screen(result_next_img, screenshot, threshold=0.85)
                        if result_next_pos:
                            print(f'result_next.png連打中→タップ ({serial})')
                            safe_tap(device, result_next_pos, team_3_pos, serial, 'result_next.png')
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
            score_1_pos = find_image_on_screen(score_1_img, screenshot, threshold=0.7)
            if score_1_pos:
                box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.7)
                if box_key_close_pos:
                    print(f'score_1.png検出→box-key_list_close.pngタップ ({serial})')
                    safe_tap(device, box_key_close_pos, team_3_pos, serial, 'box-key_list_close.png')
                else:
                    print(f'score_1.png検出したがbox-key_list_close.png見つからず ({serial})')
                continue
            
            # ③score_redJ.pngを検知したらscore_close.pngをタップ
            score_redJ_pos = find_image_on_screen(score_redJ_img, screenshot, threshold=0.7)
            if score_redJ_pos:
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.7)
                if score_close_pos:
                    print(f'score_redJ.png検出→score_close.pngタップ ({serial})')
                    tap(device, score_close_pos)
                else:
                    print(f'score_redJ.png検出したがscore_close.png見つからず ({serial})')
                continue
            
            # ④ranking.pngを検知したらscore_close.pngをタップ
            ranking_pos = find_image_on_screen(ranking_img, screenshot, threshold=0.6)
            if ranking_pos:
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.7)
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
            koukan_2_pos = find_image_on_screen(koukan_2_img, screenshot, threshold=0.7)
            if koukan_2_pos:
                score_close_pos = find_image_on_screen(score_close_img, screenshot, threshold=0.7)
                if score_close_pos:
                    print(f'koukan_2.png検出→score_close.pngタップ ({serial})')
                    tap(device, score_close_pos)
                else:
                    print(f'koukan_2.png検出したがscore_close.png見つからず ({serial})')
                continue
            
            # ⑦team.pngを検知したらbox-key_list_close.pngをタップ
            team_pos = find_image_on_screen(team_img, screenshot, threshold=0.7)
            if team_pos:
                box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.7)
                if box_key_close_pos:
                    print(f'team.png検出→box-key_list_close.pngタップ ({serial})')
                    safe_tap(device, box_key_close_pos, team_3_pos, serial, 'box-key_list_close.png')
                else:
                    print(f'team.png検出したがbox-key_list_close.png見つからず ({serial})')
                continue
            
            # ⑧yubin.pngを検知したらbox-key_list_close.pngをタップ
            yubin_pos = find_image_on_screen(yubin_img, screenshot, threshold=0.8)
            if yubin_pos:
                box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
                if box_key_close_pos:
                    print(f'yubin.png検出→box-key_list_close.pngタップ ({serial})')
                    safe_tap(device, box_key_close_pos, team_3_pos, serial, 'box-key_list_close.png')
                else:
                    print(f'yubin.png検出したがbox-key_list_close.png見つからず ({serial})')
                continue
            
            # ⑨box-key_list_close.pngを検知したら直接タップ
            box_key_close_pos = find_image_on_screen(box_key_list_close_img, screenshot, threshold=0.8)
            if box_key_close_pos:
                print(f'box-key_list_close.png検出→タップ ({serial})')
                safe_tap(device, box_key_close_pos, team_3_pos, serial, 'box-key_list_close.png')
                continue
            
            # home.png/google_play.png/google_login.png/gmail.pngが出ていたらクラッシュ復旧
            # 閾値を厳しくして誤検知を減らす（単一画像での判定）
            home_pos = find_image_on_screen(home_img, screenshot, threshold=0.95)
            google_play_pos = find_image_on_screen(google_play_img, screenshot, threshold=0.95)
            google_login_pos = find_image_on_screen(google_login_img, screenshot, threshold=0.95)
            gmail_pos = find_image_on_screen(gmail_img, screenshot, threshold=0.95)
            
            if home_pos or google_play_pos or google_login_pos or gmail_pos:
                print(f'クラッシュ復帰処理を実行します... ({serial})')
                crash_recovery(device)
        except Exception as e:
            print(f'デバイス {serial} でエラー: {e}')
        time.sleep(0.00417)  # 約0.00417秒間隔（1秒に240回実行）

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
