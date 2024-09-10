from nonebot.rule import to_me
from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession
from nonebot_plugin_alconna import (Args, Match, Query, Option, Alconna, Arparma, Subcommand, AlconnaQuery, on_alconna, store_true, At)
from zhenxun.services.log import logger
from zhenxun.utils.enum import BlockType, PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.depends import UserName
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.configs.utils import RegisterConfig, PluginExtraData, BaseBlock
from zhenxun.utils.rules import ensure_group
import re
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
from nonebot.plugin import PluginMetadata

# from services.log import logger

from .utils import *
from .start import *



__plugin_meta__ = PluginMetadata(
    name="赛马",
    description="真寻的赛马场[今日份的梦中情马]",
    usage="""
    赛马养成指令：
        获取赛马[马的称号][马的全名]：获得一匹赛马
        我的赛马：显示我的赛马
        赛马改名[马的称号][马的全名]：赛马重命名
        刷新赛马数据：刷新赛马四维属性
    赛马活动指令：（群限定）
        

    管理员指令：赛马事件重载
    
    """.strip(),
    extra=PluginExtraData(
        author="冥乐",
        version="3.0",
        plugin_type=PluginType.NORMAL,
        menu_type="赛马",
        # limits=[BaseBlock(check_type=BlockType.GROUP)],
    ).dict(),
)


# RaceReStart = on_command("赛马重置", priority=5, block=True)
# RaceStop = on_command("赛马暂停", priority=5, permission=SUPERUSER, block=True)
# RaceClear = on_command("赛马清空", priority=5, permission=SUPERUSER, block=True)
# RaceReload = on_command("赛马事件重载", priority=5, permission=SUPERUSER, block=True)

# 赛马培养=======================================================================
_matcher_horse = on_alconna(
    Alconna(
        "赛马",
        Subcommand("new-horse", Args["name?", str, ""]["nickname?", str, ""], help_text="获取赛马"),
        Subcommand("my-horse", help_text="我的赛马"),
        Subcommand("rename-horse", Args["name?", str, ""]["nickname?", str, ""], help_text="赛马改名"),
        Subcommand("refresh-horse", help_text="刷新赛马数据"),
    ),
    priority=5,
    block=True,
)
_matcher_horse.shortcut(
    "获取赛马",
    command="赛马",
    arguments=["new-horse"],
    prefix=True,
)
_matcher_horse.shortcut(
    "我的赛马",
    command="赛马",
    arguments=["my-horse"],
    prefix=True,
)
_matcher_horse.shortcut(
    "赛马改名",
    command="赛马",
    arguments=["rename-horse"],
    prefix=True,
)
_matcher_horse.shortcut(
    "刷新赛马数据",
    command="赛马",
    arguments=["refresh-horse"],
    prefix=True,
)
_matcher_race = on_alconna(
    Alconna(
        "赛马",
        Subcommand("race-setup", help_text="赛马创建"),
        Subcommand("race-join", help_text="赛马加入"),
        Subcommand("race-start", help_text="赛马开始"),
    ),
    priority=5,
    block=True,
    rule=ensure_group,
)
_matcher_race.shortcut(
    "赛马创建",
    command="赛马",
    arguments=["race-setup"],
    prefix=True,
)
_matcher_race.shortcut(
    "赛马加入",
    command="赛马",
    arguments=["race-join"],
    prefix=True,
)
_matcher_race.shortcut(
    "赛马开始",
    command="赛马",
    arguments=["race-start"],
    prefix=True,
)
_matcher_super = on_alconna(
    Alconna(
        "赛马",
        Subcommand("event-del", help_text="赛马事件清空"),
        Subcommand("event-reload", help_text="赛马事件重载"),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)
_matcher_super.shortcut(
    "赛马事件重载",
    command="赛马",
    arguments=["event-reload"],
    prefix=True,
)


# ================================以下为正式函数================================
# 此项为已经加载的事件列表，暂定
# event_list = []




@_matcher_horse.assign("new-horse")
async def _(session: EventSession, arparma: Arparma, name: str, nickname: str):
    result = await new_horse(session.id1, name, nickname)
    await MessageUtils.build_message(result).finish(at_sender=True)


@_matcher_horse.assign("my-horse")
async def _(session: EventSession, arparma: Arparma):
    result = await show_horse(session.id1)
    await MessageUtils.build_message(result).send(at_sender=True)

@_matcher_horse.assign("rename-horse")
async def _(session: EventSession, arparma: Arparma, name: str, nickname: str):
    result = await rename_horse(session.id1, name, nickname)
    await MessageUtils.build_message(result).send(at_sender=True)


@_matcher_horse.assign("refresh-horse")
async def _(session: EventSession, arparma: Arparma):
    result = await refresh_horse(session.id1)
    await MessageUtils.build_message(result).send(at_sender=True)


@_matcher_race.assign("race-setup")
async def _(session: EventSession, arparma: Arparma):
    result = ""
    await MessageUtils.build_message(result).send(at_sender=True)


@_matcher_race.assign("race-join")
async def _(session: EventSession, arparma: Arparma):
    result = ""
    await MessageUtils.build_message(result).send(at_sender=True)


@_matcher_race.assign("race-start")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    user_id = session.id1
    group_id = session.id2
    result = f"{nickname}发起了一场赛马\n请输入“赛马加入”加入比赛\n赛马场需要一分钟准备场地，请耐心等待人员加入“”"
    await MessageUtils.build_message(result).send(at_sender=True)
    logger.info(f"群[{group_id}]/玩家[{nickname}][{user_id}]发起了赛马活动")
    # 读取事件表：
    await get_event()
    # 读取
    # "rare": 0,默认值，填0为普通事件，-1为不会主动随机触发的子事件
    # "rare": 1,填1为降低触发率的高稀有度事件
    # "rare": -1,填-1为不会主动随机触发的事件，仅作为子事件被其他事件触发

    # result = await race_start()



@_matcher_super.assign("event-del")
async def _(session: EventSession, arparma: Arparma):
    result = await load_dlcs()
    await MessageUtils.build_message(result).send(at_sender=True)

@_matcher_super.assign("event-reload")
async def _(session: EventSession, arparma: Arparma):
    await Eventdb.filter().delete()
    result = await load_dlcs()
    await MessageUtils.build_message(result).send(at_sender=True)






# ================================以上为正式函数================================
# ================================以下函数未启用================================
# ================================以下函数未启用================================
# ================================以下函数未启用================================
# ================================以下函数未启用================================


_matcher_test = on_alconna(
    Alconna(
        "赛马",
        Subcommand("test1"),
        Subcommand("test2"),
        Subcommand("test3"),
        Subcommand("test4", Args["level", int, ""]["a0", str, ""]["a1", str, ""]["a2", str, ""]["a3", str, ""]),
        Subcommand("test5"),
    ),
    priority=5,
    block=True,
    # rule=ensure_group,
)


_matcher_test.shortcut(
    "1",
    command="赛马",
    arguments=["test1"],
    prefix=True,
)
_matcher_test.shortcut(
    "2",
    command="赛马",
    arguments=["test2"],
    prefix=True,
)
_matcher_test.shortcut(
    "3",
    command="赛马",
    arguments=["test3"],
    prefix=True,
)
_matcher_test.shortcut(
    "4",
    command="赛马",
    arguments=["test4"],
    prefix=True,
)
_matcher_test.shortcut(
    "5",
    command="赛马",
    arguments=["test5"],
    prefix=True,
)

@_matcher_test.assign("test1")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    pass
    user_id = session.id1
    await horse_getexp(user_id,430)
    await MessageUtils.build_message("测试指令，获取430经验").send()

@_matcher_test.assign("test2")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    pass
    user_id = session.id1
    horse = await get_horse(user_id)
    result = await horse_refresh_rate(horse)        #刷新属性

    await MessageUtils.build_message(result).send(at_sender=True)

@_matcher_test.assign("test3")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    pass
    user_id = session.id1
    group_id = session.id2
    await MessageUtils.build_message(nickname).send(at_sender=True)
    await MessageUtils.build_message(user_id).send(at_sender=True)
    await MessageUtils.build_message(group_id).send(at_sender=True)
@_matcher_test.assign("test4")
async def _(session: EventSession, arparma: Arparma, level, a0, a1, a2, a3):
    pass
    result = await load_dlcs()
    await MessageUtils.build_message(str(result)).send(at_sender=True)

@_matcher_test.assign("test5")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    pass
    events = [["事件包名称", "作者"],
    {"id":["事件名称", 1],
    "sub":["horse", -1],
    "targets":["target", [], []],
    "describe":["", ""],
    "events":[{"live":1},{"die":2}],
    },
    ]


    A = [{"live": 1}, {"die": 2}]
    B = []
    [B.extend(item.keys()) for item in A]


    await MessageUtils.build_message(str(B)).send(at_sender=True)


    await asyncio.sleep(2)








# _red_bag_matcher = on_alconna(
#     Alconna("塞红包", Args["amount", int]["num", int, 5]["user?", At]),
#     aliases={"金币红包"},
#     priority=5,
#     block=True,
#     rule=ensure_group,
# )

# _open_matcher = on_alconna(
#     Alconna("开"),
#     aliases={"抢", "开红包", "抢红包"},
#     priority=5,
#     block=True,
#     rule=ensure_group,
# )
#
# _return_matcher = on_alconna(
#     Alconna("退回红包"), aliases={"退还红包"}, priority=5, block=True, rule=ensure_group
# )
#
# _festive_matcher = on_alconna(
#     Alconna(
#         "节日红包",
#         Args["amount", int]["num", int]["text?", str],
#         Option("-g|--group", Args["groups", str] / "\n", help_text="指定群"),
#     ),
#     priority=1,
#     block=True,
#     permission=SUPERUSER,
#     rule=to_me(),
# )
#
# @_matcher.assign("模板")
# async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
#     user_id = session.id1
#     group_id = session.id2
#
#     result = ""
#     await MessageUtils.build_message(result).send(at_sender=True)