import cv2

# --- 編輯模式函式 ---
def run_edit_mode(cap, command_zones, window_name, box_color):
    """
    進入編輯模式，允許使用者透過滑鼠拖拉來調整指令區塊的位置。

    :param cap: cv2.VideoCapture 物件
    :param command_zones: 當前的指令區塊列表
    :param window_name: 顯示視窗的名稱
    :param box_color: 方塊的顏色
    :return: 修改後的指令區塊列表
    """
    print("進入編輯模式... 按 's' 儲存並退出。")
    
    # 編輯模式相關變數
    editing_state = {'selected_zone': -1, 'offset': (0, 0)}
    # 複製一份以供修改，避免直接修改傳入的 list
    local_command_zones = [list(zone) for zone in command_zones]

    # 滑鼠回呼函式
    def mouse_callback(event, x, y, flags, param):
        nonlocal editing_state, local_command_zones
        
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, (zx, zy, zw, zh, name) in enumerate(local_command_zones):
                if zx <= x < zx + zw and zy <= y < zy + zh:
                    editing_state['selected_zone'] = i
                    editing_state['offset'] = (x - zx, y - zy)
                    break
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if editing_state['selected_zone'] != -1:
                i = editing_state['selected_zone']
                new_x = x - editing_state['offset'][0]
                new_y = y - editing_state['offset'][1]
                local_command_zones[i][0] = new_x
                local_command_zones[i][1] = new_y

        elif event == cv2.EVENT_LBUTTONUP:
            editing_state['selected_zone'] = -1

    cv2.setMouseCallback(window_name, mouse_callback)
    
    # 編輯模式迴圈
    while True:
        ret, edit_frame = cap.read()
        if not ret:
            print("無法讀取攝影機畫面，退出編輯模式。")
            break
        edit_frame = cv2.flip(edit_frame, 1)

        # 提示文字
        cv2.putText(edit_frame, "Editing Layout... Drag boxes with mouse.", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(edit_frame, "Press 's' to save and exit.", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 繪製目前的指令區塊
        for (x, y, w, h, name) in local_command_zones:
            cv2.rectangle(edit_frame, (x, y), (x+w, y+h), box_color, 3)
            cv2.putText(edit_frame, name, (x + 10, y + h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow(window_name, edit_frame)

        edit_key = cv2.waitKey(1) & 0xFF
        if edit_key == ord('s'):
            print("版面配置已儲存。")
            break 

    # 清除回呼函式
    cv2.setMouseCallback(window_name, lambda *args: None)
    
    # 將 list of lists 轉回 list of tuples
    return [tuple(zone) for zone in local_command_zones]
