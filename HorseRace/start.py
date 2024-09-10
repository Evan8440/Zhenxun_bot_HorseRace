from .setting import *
import math
import nonebot
from nonebot.drivers import Driver
from .horseracedb import Horsedb, Eventdb
from zhenxun.services.log import logger
import json
import os

# 默认马数据
driver: Driver = nonebot.get_driver()


@driver.on_startup
async def events_read():
    aa = [[1, "无声铃鹿", "『铃鹿』", round(level_max*0.25), 'B', 'A', 'S', 'B'],
          [2, "富士奇石", "『富士』", round(level_max*0.4), 'A', 'B', 'S', 'A'],
          [3, "里见光钻", "『光钻』", round(level_max*0.5), 'B', 'D', 'B', 'A'],
          [4, "帝王光辉", "『光辉』", round(level_max*0.6), 'A', 'C', 'A', 'C'],
          [5, "大和赤骥", "『赤骥』", round(level_max*0.8), 'C', 'S', 'B', 'B'],
          [6, "目白麦昆", "『麦昆』", round(level_max*0.8), 'B', 'A', 'D', 'B'],
          [7, "琵琶晨光", "『晨光』", round(level_max*1), 'B', 'S', 'C', 'B'],
          [8, "里见皇冠", "『皇冠』", round(level_max*1.5), 'C', 'A', 'D', 'C'],
          [9, "东海帝王", "『帝王』", round(level_max*2), 'S', 'S', 'S', 'S']]
    for A in aa:
        await Horsedb.get_or_create(user_id=A[0])
        horse, _ = await Horsedb.get_or_create(user_id=A[0])
        horse.horse_name = A[1]
        horse.horse_nickname = (A[2])
        horse.exp = A[3]
        horse.data = await pre_data(A)
        await horse.save()


async def pre_data(a):
    level = a[3]
    a0 = a[4]
    a1 = a[5]
    a2 = a[6]
    a3 = a[7]
    pa = (1 + base_rate / 100)
    pb = (1 - base_rate / 100)
    x = 1 / (1 + math.exp(-level / level_max * 4)) - 0.5
    num_0 = await rank_to_data(a0)
    rank_0 = a0
    rate_0 = round(rate_0_base - (rate_0_base * pa - rate_0_min * pb) * x * (100 + max_rate * num_0 / 100) / 100)
    num_1 = await rank_to_data(a1)
    rank_1 = a1
    rate_1 = round(rate_1_base - (rate_1_base * pa - rate_1_min * pb) * x * (100 + max_rate * num_1 / 100) / 100)
    num_2 = await rank_to_data(a2)
    rank_2 = a2
    rate_2 = round(rate_2_base + (rate_2_max * pa - rate_2_base * pb) * x * (100 + max_rate * num_2 / 100) / 100)
    num_3 = await rank_to_data(a3)
    rank_3 = a3
    rate_3 = round(rate_3_base + (rate_3_max * pa - rate_3_base * pb) * x * (100 + max_rate * num_3 / 100) / 100)
    data = [rate_0, rate_1, rate_2, rate_3, rank_0, rank_1, rank_2, rank_3, a[4], a[5], a[6], a[7]]
    return data


async def rank_to_data(a) -> int:
    if a == "S":
        return 90
    elif a == f"A":
        return 60
    elif a == f"B":
        return 35
    elif a == f"C":
        return 10
    elif a == f"D":
        return -30
    elif a == f"E":
        return -60
    else:
        return -90


@driver.on_startup
async def load_dlcs():
    logs = f""
    files = os.listdir(os.path.dirname(__file__) + '/events')
    for file in files:
        try:
            with open(f'{os.path.dirname(__file__)}/events/{file}', "r", encoding="utf-8") as f:
                logger.info(f'加载事件包文件：{file}')
                result = await deal_events(json.load(f))
                if result != f"":
                    logger.info(result)
                    logs += result
            logger.info(f"加载 {file} 成功")
            logs += f'加载 {file} 成功\n'
        except:
            logger.info(f"加载 {file} 失败！失败！失败！")
            logs += f"加载 {file} 失败！失败！失败！\n"
    return logs


async def deal_events(events) -> str:
    logs = f""
    group = events[0][0]
    length = len(events)
    i = 0
    while i < length - 1:
        i += 1
        try:
            event = events[i]
            uid = event["id"]
            try:
                try:
                    describe = event["describe"]
                except:
                    describe = ["", "", ""]
                try:
                    rare = event["rare"]
                except:
                    rare = 0
                try:
                    uniqueness = event["uniqueness"]
                except:
                    uniqueness = -1
                try:
                    sub = event["sub"]
                except:
                    sub = "horse"
                targets = event["targets"]
                data = event["events"]
                if await Eventdb.exists(group=group, uid=uid[0], name=uid[1], targets=targets,describe=describe,
                                        data=data, rare=rare, uniqueness=uniqueness, sub=sub):
                    # logs += f"id：{str(uid)}已存在，跳过\n"
                    pass
                elif await Eventdb.exists(group=group, uid=uid[0]):
                    # logs += f"id：{str(uid)}已存在，检测非重复，开始覆盖\n"
                    await Eventdb.filter(group=group, uid=uid[0]).delete()
                    await Eventdb.get_or_create(group=group, uid=uid[0], name=uid[1], targets=targets,describe=describe,
                                                data=data, rare=rare, uniqueness=uniqueness, sub=sub)
                    logs += f"Warning: id：{str(uid)}的事件加载时更新并覆盖数据，若重复此报错则为包内id重复\n"
                else:
                    await Eventdb.get_or_create(group=group, uid=uid[0], name=uid[1], targets=targets,describe=describe,
                                                data=data, rare=rare, uniqueness=uniqueness, sub=sub)
            except:
                logs += f"Warning: 事件uid:{str(uid[0])}，事件名{str(uid[1])}\n"
        except:
            logs += f"Warning: 第 {str(i)} 个事件，事件uid或事件名异常\n"

    return logs