import random
from nonebot_plugin_session import EventSession
from zhenxun.utils.depends import UserName
from .horseracedb import Horsedb
from .setting import *
import time
from .horse import RaceHorse

class RaceGroup:
    """
    比赛用群赛马场class
    """
    def __init__(self, group_id):
        self.group_id = group_id
        self.time = time.time()
        self.round = 0
        self.start = 0


        # self.player_id = []
        # self.round = 0
        # self.start = 0
        # # 0为赛前准备，1为比赛期间，2为比赛结束，不存在为比赛不存在

        self.event_uniqueness = []
        # 赛马事件，已触发的唯一性事件

    def group_id(self,):
        return self.group_id()





