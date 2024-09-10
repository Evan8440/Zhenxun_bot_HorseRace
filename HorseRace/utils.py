import re
import random
import math
from .horseracedb import Horsedb, Eventdb
from .horserace import RaceGroup
from .horse import RaceHorse
from .event import RaceEvent
from .setting import *

from nonebot_plugin_htmlrender import (
    text_to_pic,
)


def is_chinese(char):
    return bool(re.match('[\u4e00-\u9fff]', char))


async def get_horse(user_id: str)-> Horsedb:
    """
    获取数据库内马的信息，若无则无返回
    """
    if await Horsedb.exists(user_id=user_id):
        horse, _ = await Horsedb.get_or_create(user_id=user_id)
        return horse


async def new_horse(user_id: str, name: str, nickname: str) -> str:
    """
    新用户获取一匹马
    """
    if await Horsedb.exists(user_id=user_id):
        result = f"你已经有一匹马了\n请使用指令“我的赛马”查看详细"
    elif name == "":
        result = f"马的名字在哪里呢\n请使用指令：\n获取赛马 [名字] [称号]\n称号必须为2个中文字符"
    elif nickname == "":
        result = f"马的昵称又在哪里呢\n请使用指令：\n获取赛马 [名字] [称号]\n称号必须为2个中文字符"
    elif len(name) > name_max_len:
        result = f"马的名字太长了啦，最大长度是{str(name_max_len)}个中文/英文字符哒"
    elif len(nickname) != nickname_max_len or not is_chinese(nickname[:1]) or not is_chinese(nickname[1:]):
        result = f"马的昵称必须是{str(nickname_max_len)}个中文字符哒"
    else:
        horse, _ = await Horsedb.get_or_create(
            user_id=user_id, horse_name=name, horse_nickname=(f"『{nickname}』"))
        result = f"获取赛马娘成功\n{horse.horse_nickname}{horse.horse_name} 已经成为你的伙伴啦"
    return result


async def show_horse(user_id: str):
    """
    显示马的数据表
    """
    if await Horsedb.exists(user_id=user_id):
        horse = await Horsedb.get(user_id=user_id)
        data = horse.data
        horse_nickname = horse.horse_nickname
        horse_name = horse.horse_name
        exp = horse.exp
        sumx = data[0] + data[1] + data[2] + data[3]
        result = f"{horse_nickname}\n{horse_name}\n"
        result += f"Lv.{exp // exp_up_level}"
        if exp // exp_up_level < level_max:
            result += f"\nExp {exp % exp_up_level} / {exp_up_level}\n"
        else:
            result += f"  Max\n"
        result += f"综合移速：{round((data[1]  + data[2] * 2 + data[3] * 3)/ sumx * 100) / 100}\n\n"
        result += f"详细移速表：\n"
        result += f" +0\t  {data[4]}\t   {round(data[0]/sumx*100,1)}%\n"
        result += f" +1\t  {data[5]}\t   {round(data[1]/sumx*100,1)}%\n"
        result += f" +2\t  {data[6]}\t   {round(data[2]/sumx*100,1)}%\n"
        result += f" +3\t  {data[7]}\t   {round(data[3]/sumx*100,1)}%"
        return await text_to_pic(text=result, width=180, device_scale_factor=2)
    else:
        return f"您还没有自己的马，请发送“获取赛马”获得您的第一匹马"


async def rename_horse(user_id: str, name: str, nickname: str) -> str:
    """
    赛马重命名
    """
    if await Horsedb.exists(user_id=user_id):
        if name == "":
            result = f"马的名字在哪里呢\n请使用指令：\n赛马改名 [名字] [称号]\n称号必须为2个中文字符"
        elif nickname == "":
            result = f"马的昵称又在哪里呢\n请使用指令：\n赛马改名  [名字] [称号]\n称号必须为2个中文字符"
        elif len(name) > name_max_len:
            result = f"马的名字太长了啦，最大长度是{str(name_max_len)}个中文/英文字符哒"
        elif len(nickname) != nickname_max_len or not is_chinese(nickname[:1]) or not is_chinese(nickname[1:]):
            result = f"马的昵称必须是{str(nickname_max_len)}个中文字符哒"
        else:
            horse, _ = await Horsedb.get_or_create(
                user_id=user_id, horse_name=name, horse_nickname=("『" + nickname + "』"))
            result = f"赛马改名成功\n{horse.horse_nickname}{horse.horse_name} 又是个名字响亮的崽啦"
    else:
        result = f"您还没有自己的马，请发送“获取赛马”获得您的第一匹马"
    return result


async def random_rank() -> [int, str]:
    """
    rank分级
    """
    a = random.randint(0, 100)
    return await num_to_rank(a)


async def num_to_rank(a) -> [int, str]:
    if a >= 90:
        rank = "S"
    elif a >= 75:
        rank = "A"
    elif a >= 60:
        rank = "B"
    elif a >= 40:
        rank = "C"
    elif a >= 25:
        rank = "D"
    elif a >= 10:
        rank = "E"
    else:
        rank = "F"
    return [a, rank]

async def horse_refresh_rate(horse: Horsedb):
    """
    刷新属性，适用于手刷属性
    返回pic
    """
    level = horse.exp // exp_up_level
    pa = (1 + base_rate / 100)
    pb = (1 - base_rate / 100)
    x = 1 / (1 + math.exp(-level / level_max * 4)) - 0.5
    rank = await random_rank()
    num_0 = rank[0]
    rank_0 = rank[1]
    rate_0 = round(rate_0_base - (rate_0_base * pa - rate_0_min * pb) * x * (1 + max_rate * (rank[0] - 50)/5000))
    rank = await random_rank()
    num_1 = rank[0]
    rank_1 = rank[1]
    rate_1 = round(rate_1_base - (rate_1_base * pa - rate_1_min * pb) * x * (1 + max_rate * (rank[0] - 50)/5000))
    rank = await random_rank()
    num_2 = rank[0]
    rank_2 = rank[1]
    rate_2 = round(rate_2_base + (rate_2_max * pa - rate_2_base * pb) * x * (1 + max_rate * (rank[0] - 50)/5000))
    rank = await random_rank()
    num_3 = rank[0]
    rank_3 = rank[1]
    rate_3 = round(rate_3_base + (rate_3_max * pa - rate_3_base * pb) * x * (1 + max_rate * (rank[0] - 50)/5000))
    data = [rate_0, rate_1, rate_2, rate_3, rank_0, rank_1, rank_2, rank_3, num_0, num_1, num_2, num_3]
    horse.data = data
    await horse.save()
    horse_nickname = horse.horse_nickname
    horse_name = horse.horse_name
    exp = horse.exp
    sumx = data[0] + data[1] + data[2] + data[3]
    result = f"{horse_nickname}\n{horse_name}\n"
    result += f"Lv.{exp // exp_up_level}"
    if exp // exp_up_level < level_max:
        result += f"\n\n"
    else:
        result += f"  Max\n\n"
    result += f"本次刷新能力值：\n"
    # result += f"移动|Rank|权重|概率占比\n"
    # result += f" +0\t  {data[4]}\t  {data[0]}\t   {round(data[0]/sumx*100, 1)}%\n"
    # result += f" +1\t  {data[5]}\t  {data[1]}\t   {round(data[1]/sumx*100, 1)}%\n"
    # result += f" +2\t  {data[6]}\t  {data[2]}\t   {round(data[2]/sumx*100, 1)}%\n"
    # result += f" +3\t  {data[7]}\t  {data[3]}\t   {round(data[3]/sumx*100, 1)}%\n"
    result += f"移动|Rank|权重\n"
    result += f" +0\t  {data[4]}\t  {data[0]}\n"
    result += f" +1\t  {data[5]}\t  {data[1]}\n"
    result += f" +2\t  {data[6]}\t  {data[2]}\n"
    result += f" +3\t  {data[7]}\t  {data[3]}\n"
    result += f"综合移速{round((data[1]  + data[2] * 2 + data[3] * 3)/ sumx * 100) / 100}"
    return await text_to_pic(text=result, width=180, device_scale_factor=2)


async def horse_getexp(user_id: str, exp: int):
    """
    马获得经验，不带升级判定
    """
    if await Horsedb.exists(user_id=user_id):
        horse = await get_horse(user_id)
        level_0 = horse.exp // exp_up_level
        horse.exp += exp
        if horse.exp > level_max * exp_up_level:
            horse.exp = level_max * exp_up_level
        await horse.save()
        level_1 = horse.exp // exp_up_level
        if level_1 > level_0:
            data = horse.data
            pa = (1 + base_rate / 100)
            pb = (1 - base_rate / 100)
            x = 1 / (1 + math.exp(-level_1 / level_max * 4)) - 0.5
            rank_0 = (await num_to_rank(data[8]))[1]
            rate_0 = round(rate_0_base - (rate_0_base * pa - rate_0_min * pb) * x * (1 + max_rate * (data[8] - 50) / 5000))
            rank_1 = (await num_to_rank(data[9]))[1]
            rate_1 = round(rate_1_base - (rate_1_base * pa - rate_1_min * pb) * x * (1 + max_rate * (data[9] - 50) / 5000))
            rank_2 = (await num_to_rank(data[10]))[1]
            rate_2 = round(rate_2_base + (rate_2_max * pa - rate_2_base * pb) * x * (1 + max_rate * (data[10] - 50) / 5000))
            rank_3 = (await num_to_rank(data[11]))[1]
            rate_3 = round(rate_3_base + (rate_3_max * pa - rate_3_base * pb) * x * (1 + max_rate * (data[11] - 50) / 5000))
            horse.data = [rate_0, rate_1, rate_2, rate_3, rank_0, rank_1, rank_2, rank_3, data[8], data[9], data[10], data[11]]
            await horse.save()
        else:
            pass




# ================================以上为正式函数================================
# ================================以下函数未启用================================


async def get_horse_class(user_id: str):
    """
    获取数据库内马的信息，class:racehorse形式，若无则无返回
    """
    if await Horsedb.exists(user_id=user_id):
        horse = await get_horse(user_id)
        result = RaceHorse(horse.id, horse.user_id, horse.horse_name, horse.horse_nickname, horse.exp, horse.data)
        return result
    else:
        pass


# async def get_horse_dict(user_id: str):
#     """
#     获取数据库内马的信息，racehorse形式，若无则无返回
#     """
#     if await Horsedb.exists(user_id=user_id):
#         horse = await get_horse(user_id)
#         result = {"id": horse.id,
#                   "owner": horse.user_id,
#                   "name": horse.horse_name,
#                   "nickname": horse.horse_nickname,
#                   "exp": horse.exp,
#                   "data": horse.data
#                   }
#         return result
#     else:
#         pass


async def get_event(user_id: str) -> Eventdb:
    """
    获取数据库内event的信息，若无则无返回
    """
    if await Eventdb.exists(id=id):
        event, _ = await Eventdb.get_or_create(id=id)
        return event


async def horse_race_event(RaceGroup: RaceGroup, RaceHorse: int | RaceHorse, RaceEvent: RaceEvent):
    pass
    group_id = RaceGroup.group_id()

    horse_id = RaceHorse.id

    if isinstance(RaceHorse, int):
        pass
        # 判定为假马或预设马
    else:
        pass
        # 真马


    # id = fields.IntField(pk=True, generated=True, auto_increment=True)
    # """自增id"""
    # group = fields.CharField(255, null=True, description="事件包全名")
    # """事件包名称"""
    # uid = fields.IntField(default=0, description="事件包内编号")
    # """事件包内编号"""
    # name = fields.CharField(255, null=True, description="事件名")
    # """事件名"""
    # sub = fields.CharField(255, null=True, description="事件主体")
    # """事件主体"""
    # uniqueness = fields.IntField(default=0, description="事件唯一型值")
    # """事件唯一型值"""
    # targets: Dict[str, int] = fields.JSONField(default={}, description="事件目标")
    # """事件Dict-target"""
    # data: Dict[str, int] = fields.JSONField(default={}, description="事件内容")
    # """事件Dict-data"""