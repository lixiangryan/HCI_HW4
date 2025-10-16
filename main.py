import cv2
import numpy as np
import time

# --- 參數設定 ---
CAP_WIDTH = 1280
CAP_HEIGHT = 720
BOX_COLOR = (255, 0, 255) # 亮粉色
COMMAND_ZONES = [
    (100, 150, 200, 100, "拍照 (Take Photo)"),
    (100, 300, 200, 100, "播放影片 (Play Video)"),
    (100, 450, 200, 100, "結束程式 (Exit)"),
]
TRIGGER_THRESHOLD = 30
ACCUMULATION_RATE = 1
DECAY_RATE = 2
GET_READY_SECONDS = 3    # 按下按鍵後的準備時間
CALIBRATION_SECONDS = 3  # 正式校準時間
VAR_THRESHOLD = 75
CAMERA_WAIT_TIMEOUT = 10 # 等待攝影機啟動的最長時間（秒）

# --- 繪圖函式 ---
def draw_ui(frame, zones, accumulators=None, threshold=None):
    for i, (x, y, w, h, name) in enumerate(zones):
        if accumulators is not None and threshold is not None:
            progress = min(accumulators[i] / threshold, 1.0)
            if progress > 0:
                cv2.rectangle(frame, (x, y), (x + int(w * progress), y + h), BOX_COLOR, -1)
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), BOX_COLOR, 3)
        cv2.putText(frame, name, (x + 10, y + h - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# --- 程式主體 ---
def main():
    # --- 修改：耐心等待攝影機啟動 ---
    print("正在啟動攝影機，這可能需要幾秒鐘...")
    cap = cv2.VideoCapture(0)
    
    start_time = time.time()
    camera_ready = False
    while time.time() - start_time < CAMERA_WAIT_TIMEOUT:
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                camera_ready = True
                break
        # 短暫延遲，避免 CPU 占用過高
        time.sleep(0.1)

    if not camera_ready:
        print(f"錯誤：在 {CAMERA_WAIT_TIMEOUT} 秒內無法從攝影機讀取畫面。")
        print("請檢查攝影機是否被其他程式占用，或重新插拔攝影機。")
        cap.release()
        return

    print("攝影機已成功啟動！")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)
    
    backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=VAR_THRESHOLD, detectShadows=False)

    # 階段一：等待使用者按下按鍵
    while True:
        ret, frame = cap.read()
        if not ret: continue
        
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "Press 's' to start calibration", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        draw_ui(frame, COMMAND_ZONES)
        cv2.imshow("Hand Gesture Interface", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            print("收到指令！準備開始校準...")
            break
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

    # 階段二：給使用者準備的倒數計時
    start_time = time.time()
    while time.time() - start_time < GET_READY_SECONDS:
        ret, frame = cap.read()
        if not ret: continue
        
        frame = cv2.flip(frame, 1)
        remaining_time = GET_READY_SECONDS - int(time.time() - start_time)
        cv2.putText(frame, f"Get Ready! Calibration starts in: {remaining_time}", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        draw_ui(frame, COMMAND_ZONES)
        cv2.imshow("Hand Gesture Interface", frame)
        cv2.waitKey(1)

    # 階段三：正式校準
    print(f"即將進行 {CALIBRATION_SECONDS} 秒背景校準，請保持畫面靜止...")
    start_time = time.time()
    while time.time() - start_time < CALIBRATION_SECONDS:
        ret, frame = cap.read()
        if not ret: continue
        
        frame = cv2.flip(frame, 1)
        remaining_time = CALIBRATION_SECONDS - int(time.time() - start_time)
        cv2.putText(frame, f"Calibrating... Keep Still: {remaining_time}", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        draw_ui(frame, COMMAND_ZONES)
        cv2.imshow("Hand Gesture Interface", frame)
        cv2.waitKey(1)
        
        blur_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        backSub.apply(blur_frame)

    print("校準完成，可以開始操作！")
    zone_accumulators = [0] * len(COMMAND_ZONES)

    # 階段四：主偵測迴圈
    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        blur_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        fg_mask = backSub.apply(blur_frame)
        fg_mask = cv2.erode(fg_mask, None, iterations=2)
        fg_mask = cv2.dilate(fg_mask, None, iterations=2)

        for i, (x, y, w, h, name) in enumerate(COMMAND_ZONES):
            roi_mask = fg_mask[y:y+h, x:x+w]
            motion_detected = cv2.countNonZero(roi_mask)

            if motion_detected > (w * h * 0.1): zone_accumulators[i] += ACCUMULATION_RATE
            else: zone_accumulators[i] = max(0, zone_accumulators[i] - DECAY_RATE)

            if zone_accumulators[i] > TRIGGER_THRESHOLD:
                print(f"指令觸發: {name}")
                if name == "結束程式 (Exit)":
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                zone_accumulators[i] = 0
        
        draw_ui(frame, COMMAND_ZONES, zone_accumulators, TRIGGER_THRESHOLD)

        cv2.imshow("Hand Gesture Interface", frame)
        cv2.imshow("Foreground Mask", fg_mask) 

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
    print("程式已結束。")

if __name__ == '__main__':
    main()