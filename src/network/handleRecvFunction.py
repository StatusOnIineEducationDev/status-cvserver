import random

from src.network.edu import *
from src.network.connection import *
from src.utils.base64_decode import base64ToImg
from src.model.concentration import *


def studentCameraFrameData(connection, json_obj):
    img = base64ToImg(base64_str=json_obj["frame_mat"])
    concentration_main(img)

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
