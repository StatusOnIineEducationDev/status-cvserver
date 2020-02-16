import random

from src.server.service.conc import detect
from src.server.socket.edu import TransportCmd
from src.server.socket.socket_utils import send
from src.utils.base64_decode import base64ToImg


def handleRecvData(conn, json_obj):
    """ 处理接收到的数据包

        根据数据包中command不同
        作出相应的处理
    :param conn: socket连接
    :param json_obj: 数据包中的json格式数据
    :return:
    """
    command = json_obj["command"]

    if command is TransportCmd.StudentCameraFrameData:
        studentCameraFrameData(conn, json_obj)


def studentCameraFrameData(conn, json_obj):
    """ 处理主服务器发送过来的帧数据

    :param conn: socket连接
    :param json_obj: 数据包
    :return:
    """
    img = base64ToImg(base64_str=json_obj['frame_mat'])

    detect(img=img, uid=json_obj['uid'], course_id=json_obj['course_id'],
           lesson_id=json_obj['lesson_id'], timestamp=json_obj['concentration_timestamp'])

    return_data = {
        'command': TransportCmd.ConcentrationFinalData,
        'course_id': json_obj['course_id'],
        'lesson_id': json_obj['lesson_id'],
        'uid': json_obj['uid'],
        'concentration_value': random.randint(0, 100),
        'fatigue_value': random.randint(0, 100),
        'toward_score': random.randint(0, 100),
        'emotion_score': random.randint(0, 100),
        'concentration_timestamp': json_obj["concentration_timestamp"]
    }

    send(conn, return_data)