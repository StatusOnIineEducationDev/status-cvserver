import random

from src.socket.edu import TransportCmd
from src.socket.connection import *
from src.utils.base64_decode import base64ToImg
from src.face_detection.interface import *


def studentCameraFrameData(connection, json_obj):
    uid = json_obj["uid"]
    img = base64ToImg(base64_str=json_obj["frame_mat"])

    pic_judge, emotion_index, is_blink, is_yawn, h_angle, v_angle = concentration_main(image)

    return_data = {
        "command": TransportCmd.ConcentrationFinalData,
        "course_id": json_obj["course_id"],
        "lesson_id": json_obj["lesson_id"],
        "uid": json_obj["uid"],
        "concentration_value": random.randint(0, 100),
        "fatigue_value": random.randint(0, 100),
        "toward_score": random.randint(0, 100),
        "emotion_score": random.randint(0, 100),
        "concentration_timestamp": json_obj["concentration_timestamp"]
    }

    reply(connection, return_data)
