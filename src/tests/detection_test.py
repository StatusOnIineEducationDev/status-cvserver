import cv2

from src.face_detection.interface import concentration_main, concentration_calculation
from src.server.socket.connection import connect

if __name__ == '__main__':
    # 测试
    cap = cv2.VideoCapture(0)
    concentration_score = 60
    face_orientation_result = 0.0

    # 累计
    emotion_arr = [0, 0, 0, 0, 0, 0, 0]
    blink_times = 0
    yawn_times = 0
    count = 0

    # 循环获取图像，处理图像
    while cap.isOpened():
        # 读取一帧图像
        judge, image = cap.read()
        if not judge:  # 读取图像失败
            print('摄像头读取图像失败......')
            continue

        # 记录
        pic_judge, emotion_index, is_blink, is_yawn, h_angle, v_angle = concentration_main(image)
        print(pic_judge, emotion_index, is_blink, is_yawn, h_angle, v_angle)
        if pic_judge:
            emotion_arr[emotion_index] += 1
            if is_blink:
                blink_times += 1
            if is_yawn:
                yawn_times += 1

            count += 1
            if count == 10:
                print(concentration_calculation(emotion_arr, blink_times, yawn_times, h_angle, v_angle, 10))
                emotion_arr = [0, 0, 0, 0, 0, 0, 0]
                blink_times = 0
                yawn_times = 0
                count = 0

        cv2.imshow("Output", image)
        key = cv2.waitKey(50)
        if key == ord('q'):
            break
