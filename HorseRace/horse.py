
import random
from nonebot_plugin_session import EventSession
from zhenxun.utils.depends import UserName
from .horseracedb import Horsedb
from .setting import *


class RaceHorse:
    """
    比赛用马class
    """
    def __init__(self, id, owner, name, nickname, exp, data):

        self.id = id
        self.owner = owner
        self.name = name
        self.nickname = nickname
        self.exp = exp
        self.data = data





