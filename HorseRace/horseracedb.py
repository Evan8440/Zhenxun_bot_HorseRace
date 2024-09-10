from tortoise import fields
from typing import Dict
from zhenxun.services.db_context import Model
from .setting import *


class Horsedb(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, description="用户id")
    """用户id"""
    horse_name = fields.CharField(255, null=True, description="马的全名")
    """马的全名（长字符）"""
    horse_nickname = fields.CharField(255, null=True, description="马的全名")
    """马的昵称（4字符）"""
    exp = fields.IntField(default=0, description="经验")
    """总经验值"""
    data: Dict = fields.JSONField(
        default=[rate_0_base, rate_1_base, rate_2_base, rate_3_base, f"C", f"C", f"C", f"C"])
    """马的基础三维"""
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    """创建时间"""

    class Meta:
        table = "horse_race_horse"
        table_description = "赛马插件-马库"


class eventdb(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    group = fields.CharField(255, null=True, description="事件包全名")
    """事件包名称"""
    uid = fields.IntField(default=0, description="事件包内编号")
    """事件包内编号"""
    name = fields.CharField(255, null=True, description="事件名")
    """事件名"""
    targets: Dict[str, int] = fields.JSONField(default={}, description="事件目标")
    """事件目标"""
    describe = fields.CharField(255, null=True, description="事件文字")
    """事件文字"""
    data: Dict[str, int] = fields.JSONField(default={}, description="事件内容")
    """事件内容"""
    rare = fields.IntField(default=0, description="事件触发稀有度")
    """事件触发稀有度"""
    uniqueness = fields.IntField(default=0, description="事件唯一型值")
    """事件唯一型值"""
    sub = fields.CharField(255, null=True, description="事件主体")
    """事件主体"""




    class Meta:
        table = "horse_race_event"
        table_description = "赛马插件-事件库"


        """
        获取常规/稀有事件组
        await cls.filter(rare=rare)
        具体使用参考chat_history插件
        """
        #