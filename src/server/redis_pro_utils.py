from src.utils.redis_db import Redis
from src.conf.conf import REDIS_DB_NAME


class RedisForConcDetails:
    TABLE_NAME = 'CONCDETAILS'
    PRIMARY_KEY = 'UID'
    PREFIX = REDIS_DB_NAME + ':' + TABLE_NAME + ':' + PRIMARY_KEY

    def __init__(self):
        self.conn = Redis().conn

    def add(self, uid, course_id, lesson_id, timestamp, emotion,
            is_blinked, is_yawned, h_angle, v_angle):
        """
        插入一条记录

        :param uid: 用户唯一标识
        :param course_id: 课程唯一标识
        :param lesson_id: 课程下课堂唯一标识
        :param timestamp: 该条记录的时间戳（指的是图像截取的时间，而非记录生成的时间）
        :param emotion: 表情
        :param is_blinked: 是否有眨眼
        :param is_yawned: 是否有打哈欠
        :param h_angle: 头部的水平转动角度
        :param v_angle: 头部的垂直转动角度
        :return:
        """
        key = self.PREFIX + ':' + uid
        record_map = {
            'uid': uid,
            'course_id': course_id,
            'lesson_id': lesson_id,
            'timestamp': timestamp,
            'emotion': emotion,
            'is_blinked': is_blinked,
            'is_yawned': is_yawned,
            'h_angle': h_angle,
            'v_angle': v_angle
        }
        self.conn.hmset(key, record_map)

