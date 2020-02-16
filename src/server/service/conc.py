from src.face_detection.interface import concentration_main, concentration_calculation
from src.server.redis_proj_utils import RedisForConc


def detect(img, uid, course_id, lesson_id, timestamp):
    conc_score = -1

    is_succeed, emotion_index, is_blinked, is_yawned, h_angle, v_angle = concentration_main(img)
    print(is_succeed)
    redis_conc = RedisForConc()
    redis_conc.addDetails(is_succeed=is_succeed, uid=uid, course_id=course_id,
                          lesson_id=lesson_id, timestamp=timestamp, emotion=emotion_index,
                          is_blinked=is_blinked, is_yawned=is_yawned, h_angle=h_angle, v_angle=v_angle)
    if is_succeed:
        is_full, dict_list = redis_conc.addUsefulDetails(is_succeed=is_succeed, uid=uid, course_id=course_id,
                                                         lesson_id=lesson_id, timestamp=timestamp,
                                                         emotion=emotion_index,
                                                         is_blinked=is_blinked, is_yawned=is_yawned, h_angle=h_angle,
                                                         v_angle=v_angle)

        if is_full:
            emotion_arr = [0, 0, 0, 0, 0, 0, 0]
            blink_times = 0
            yawn_times = 0
            h_angle = 0
            v_angle = 0
            for record_dict in dict_list:
                # emotion保存的是表情数组的下标，以此作为arr下标，其元素加1即可
                # 至于python中的bool类型，在与int作运算时，True和False会强制转换为1和0
                emotion_arr[record_dict['emotion']] += 1
                blink_times += record_dict['is_blinked']
                yawn_times += record_dict['is_yawned']
                h_angle = record_dict['h_angle']
                v_angle = record_dict['v_angle']
            conc_score = concentration_calculation(emotion_arr=emotion_arr, close_eye_time=blink_times,
                                                   yawn_time=yawn_times, head_horizontal_rotation_angle=h_angle,
                                                   head_vertical_rotation_angle=v_angle, frequency=10)

            redis_conc.addConcRecord(uid=uid, course_id=course_id, lesson_id=lesson_id,
                                     begin_timestamp=dict_list[0]['timestamp'],
                                     end_timestamp=dict_list[-1]['timestamp'],
                                     conc_score=conc_score)

    return conc_score
