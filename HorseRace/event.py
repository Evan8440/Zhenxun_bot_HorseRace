import random
from nonebot_plugin_session import EventSession
from zhenxun.utils.depends import UserName
from .horseracedb import Horsedb, eventdb
from .setting import *
import time
from .horse import RaceHorse

class RaceEvent:
    """
    self.group = event.group 事件组
    self.uid = event.uid  事件组内编号
    self.name = event.name  事件名
    self.sub = event.sub  事件主体类型
    self.uniqueness = event.uniqueness  事件唯一性标识
    self.targets = event.targets  事件慕目标类型
    self.data = event.data   事件数据
    """
    def __init__(self, event):
        self.id = id
        # if eventdb.exists(id=id):
        #     event, _ = eventdb.get_or_create(id=id)
        self.group = event.group
        self.uid = event.uid
        self.name = event.name
        self.sub = event.sub
        self.uniqueness = event.uniqueness
        self.targets = event.targets
        self.data = event.data

    def event(self):
        return self.event




