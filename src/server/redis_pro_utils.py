import json

from src.utils.redis_db import Redis
from src.conf.conf import REDIS_DB_NAME


class RedisForConc:
    """ 封装有关专注度记录的数据库操作

        每位用户的记录在redis中以list形式存储
        一堂课的所有详细记录都将会存储在这个list中
        仅通过一个key（format: STATUS:CONCDETAILS:UID:xxx）即可以访问到该课的所有记录

        由于此格式的key是以uid作为主键的，同时也没有对其他键进行维护
        因此在redis中存储的仅是一堂课中的专注度信息，课堂结束后将转储到mysql中
    """
    PRIMARY_KEY = 'UID'
    CONC_DETAILS = 'CONCDETAILS'
    CONC = 'CONC'

    CONC_DETAILS_PREFIX = REDIS_DB_NAME + ':' + CONC_DETAILS + ':' + PRIMARY_KEY
    CONC_PREFIX = REDIS_DB_NAME + ':' + CONC + ':' + PRIMARY_KEY

    def __init__(self):
        self.conn = Redis().conn

    def addDetailsRecord(self, uid, course_id, lesson_id, timestamp, emotion,
                         is_blinked, is_yawned, h_angle, v_angle):
        """ 插入一条详细记录

            详细记录是生成最终专注度记录的依据
            每10条详细记录可用于生成1条最终记录
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
        # format: STATUS:CONCDETAILS:UID:xxx
        key = self.CONC_DETAILS_PREFIX + ':' + uid
        record_dict = {
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
        # redis的list中不能直接存储dict类型
        # 需先dict转换为str
        self.conn.lpush(key, json.dumps(record_dict))

    def addConcRecord(self, uid, course_id, lesson_id, begin_timestamp,
                      end_timestamp, conc_score):
        """ 插入一条最终记录

        :param uid: 用户唯一标识
        :param course_id: 课程唯一标识
        :param lesson_id: 课程下课堂唯一标识
        :param begin_timestamp: 该条记录生成依据的起始时间
        :param end_timestamp: 该条记录生成依据的结束时间
        :param conc_score: 专注度评分
        :return:
        """
        # format: STATUS:CONCDETAILS:UID:xxx
        key = self.CONC_PREFIX + ':' + uid
        record_dict = {
            'uid': uid,
            'course_id': course_id,
            'lesson_id': lesson_id,
            'begin_timestamp': begin_timestamp,
            'end_timestamp': end_timestamp,
            'conc_score': conc_score
        }
        # redis的list中不能直接存储dict类型
        # 需先dict转换为str
        self.conn.lpush(key, json.dumps(record_dict))
