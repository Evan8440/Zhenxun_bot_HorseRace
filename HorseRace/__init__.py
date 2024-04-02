import random
import math
import time
import json
import os
import asyncio
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent, Message, MessageSegment
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from loguru import logger
from .start import *
from .race_group import race_group
from .setting import  *
from ..nonebot_plugin_htmlrender import text_to_pic

__zx_plugin_name__ = "赛马"
__plugin_usage__ = """
usage：
    第一位玩家发起活动，指令：赛马创建
    加入赛马活动指令：赛马加入 [你的马儿名称]
    开始指令：赛马开始
    赛马超时重置指令：赛马重置

    管理员指令：赛马暂停/赛马清空
                    赛马事件重载
""".strip()
__plugin_des__ = "真寻小赌场-赛马场"
__plugin_cmd__ = ["赛马创建/加入[名称]/开始"]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 2.1
__plugin_author__ = "冥乐"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["赛马"],
}
events_list = []
#开场加载
driver=get_driver()
@driver.on_startup
async def events_read():
    global events_list
    events_list = await load_dlcs()


RaceNew = on_command("赛马创建", priority=5, block=True)
RaceJoin = on_command("赛马加入",priority=5, block=True)
RaceStart = on_command("赛马开始", priority=5, block=True)
RaceReStart = on_command("赛马重置", priority=5, block=True)
RaceStop = on_command("赛马暂停", priority=5, permission=SUPERUSER, block=True)
RaceClear = on_command("赛马清空", priority=5, permission=SUPERUSER, block=True)
RaceReload = on_command("赛马事件重载", priority=5, permission=SUPERUSER, block=True)
race = {}

@RaceNew.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global race
    group = event.group_id
    try:
        if race[group].start == 0 and time.time() - race[group].time < 300:
            over_time = math.ceil(time.time() - race[group].time)
            out_msg = f'> 创建赛马比赛失败!\n> 原因:赛马已经创建\n> 解决方案:创不起就加入...\n> 也可以输入“赛马重置”'
            if over_time < setting_over_time:
                out_msg = f'> 创建赛马比赛失败!\n> 原因:赛马已经创建\n> 解决方案:创不起就加入...\n> 也可以在{str(setting_over_time - over_time)}秒后输入 赛马重置'
            await RaceNew.finish(out_msg)
        elif race[group].start == 1 :
            await RaceNew.finish(f"> 创建赛马比赛失败！一场赛马正在进行中\n> 如赛马已经卡死，请在超时后输入“赛马重置”")
            await RaceNew.finish()
    except KeyError:
        pass
    race[group] = race_group()
    await RaceNew.finish(f'> 创建赛马比赛成功\n> 输入 赛马加入+名字 即可加入赛马')

@RaceJoin.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global race, max_player
    msg = arg.extract_plain_text().strip()
    uid = event.user_id
    group = event.group_id
    player_name = event.sender.card if event.sender.card else event.sender.nickname
    try:
        race[group]
    except KeyError:
        await RaceJoin.finish( f"赛马活动未开始，请输入“赛马创建”开场")
    try:
        if race[group].start == 1 or race[group].start == 2:
            await RaceJoin.finish()
    except KeyError:
        await RaceJoin.finish()
    if race[group].query_of_player() >= max_player:
        await RaceJoin.finish( f"> 加入失败\n> 原因:赛马场就那么大，满了满了！" )
    if race[group].is_player_in(uid) == True:
        await RaceJoin.finish( f"> 加入失败\n> 原因:您已经加入了赛马场!")
    if msg:
        horse_name = msg
    else:
        await RaceJoin.finish(f"请输入你的马儿名字", at_sender=True)
    if race[group].is_horse_in(msg) == True:
        await RaceJoin.finish( f"> 加入失败\n> 原因:有一匹同名的马儿加入了赛马场!")
    if len(msg) > name_max_len:
        await RaceJoin.finish(f'> 加入失败\n> 原因:马儿名字太长了\n> 不可以超过{name_max_len}个字哦')
    if msg[:1] == f'.':
        await RaceJoin.finish(f'> 加入失败\n> 原因:马儿名字不可以用“.”开头哦')
    if msg[len(msg) - 1:] == f'.':
        await RaceJoin.finish(f'> 加入失败\n> 原因:马儿名字不可以用“.”结尾哦')
    race[group].add_player(horse_name, uid, player_name)
    out_msg = f'> 加入赛马成功\n> 赌上马儿性命的一战即将开始!\n> 赛马场位置:{str(race[group].query_of_player())}/{str(max_player)}'
    await RaceJoin.finish(out_msg, at_sender=True)

@RaceStart.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global race
    global events_list
    group = event.group_id
    try:
        if race[group].query_of_player() == 0:
            await RaceStart.finish()
    except KeyError:
        await RaceStart.finish()
    try:
        if race[group].start == 0 or race[group].start == 2:
            if len(race[group].player) >= min_player:
                race[group].start_change(1)
            else:
                await RaceStart.finish(f'> 开始失败\n> 原因:赛马开局需要最少{str(min_player)}人参与', at_sender=True)
        elif race[group].start == 1:
            await RaceStart.finish()
    except KeyError:
        await RaceStart.finish()
    race[group].time = time.time()
    while race[group].start == 1:
#显示器初始化
        display = f""
# 回合数+1
        race[group].round_add()
#移除超时buff
        race[group].del_buff_overtime()
#马儿全名计算
        race[group].fullname()
#回合事件计算
        display += race[group].event_start(events_list)
#马儿移动
        race[group].move()
#场地显示
        display += race[group].display()
        logger.info(f'事件输出:\n {display}')
        await RaceStart.send(MessageSegment.image(await text_to_pic(display, None, 300)))
        await asyncio.sleep(2)
#全员失败计算
        if race[group].is_die_all():
            del race[group]
            await RaceStart.finish("比赛已结束，鉴定为无马生还")
#全员胜利计算
        winer = race[group].is_win_all()
        if winer != f"":
            await RaceStart.send(f'> 比赛结束\n> 赫尔正在为您生成战报...')
            await asyncio.sleep(2)
            del race[group]
            msg = "比赛已结束，胜者为：" + winer
            await RaceStart.finish(msg)
        await asyncio.sleep(4)

@RaceReStart.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    global race
    group = event.group_id
    time_key = math.ceil(time.time() - race[group].time)
    if time_key >= setting_over_time:
        del race[group]
        await RaceReStart.finish(f'超时{str(setting_over_time)}秒，准许重置赛马场')
    await RaceReStart.finish(f'未超时{str(setting_over_time)}秒，目前为{str(time_key)}秒，未重置')

@RaceStop.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global race
    group = event.group_id
    race[group].start_change(2)

@RaceClear.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    global race
    group = event.group_id
    del race[group]

@RaceReload.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    global events_list
    logs = f""
    files = os.listdir(os.path.dirname(__file__) + '/events')
    for file in files:
        try:
            with open(f'{os.path.dirname(__file__)}/events/{file}', "r", encoding="utf-8") as f:
                logger.info(f'加载事件文件：{file}')
                events = deal_events(json.load(f))
                events_list.extend(events)
            logger.info(f"加载 {file} 成功")
            logs += f'加载 {file} 成功\n'
        except:
            logger.info(f"加载 {file} 失败！失败！失败！")
            logs += f"加载 {file} 失败！失败！失败！\n"
    await RaceReload.finish(logs)

