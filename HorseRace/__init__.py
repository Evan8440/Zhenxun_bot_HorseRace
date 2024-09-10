

from nonebot.rule import to_me
from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession
from nonebot_plugin_alconna import (
    Args,
    Match,
    Query,
    Option,
    Alconna,
    Arparma,
    Subcommand,
    AlconnaQuery,
    on_alconna,
    store_true,
)
from zhenxun.services.log import logger
from zhenxun.utils.enum import BlockType, PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.depends import UserName
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.configs.utils import RegisterConfig, PluginExtraData, BaseBlock
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
    获取赛马[马的称号][马的全名]：获得一匹赛马
    我的赛马：显示我的赛马
    赛马改名[马的称号][马的全名]：赛马重命名
    备注：称号2中文字符，名称16字符以内
    
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


_matcher = on_alconna(
    Alconna(
        "赛马",
        Subcommand("new-horse", Args["name?", str, ""]["nickname?", str, ""], help_text="获取赛马"),
        Subcommand("my-horse", help_text="我的赛马"),
        Subcommand("rename-horse", Args["name?", str, ""]["nickname?", str, ""], help_text="赛马改名"),
        # Subcommand("my-props", help_text="我的道具"),
        # Subcommand("buy", Args["name", str]["num", int, 1], help_text="购买道具"),
        # Subcommand("use", Args["name", str]["num?", int, 1], help_text="使用道具"),
        Subcommand("test1"),
        Subcommand("test2"),
        Subcommand("test3"),
        Subcommand("test4", Args["level", int, ""]["a0", str, ""]["a1", str, ""]["a2", str, ""]["a3", str, ""]),
        Subcommand("test5"),
    ),
    priority=5,
    block=True,
)


_matcher.shortcut(
    "获取赛马",
    command="赛马",
    arguments=["new-horse"],
    prefix=True,
)
_matcher.shortcut(
    "我的赛马",
    command="赛马",
    arguments=["my-horse"],
    prefix=True,
)
_matcher.shortcut(
    "赛马改名",
    command="赛马",
    arguments=["rename-horse"],
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




@_matcher.assign("new-horse")
async def _(session: EventSession, arparma: Arparma, name: str, nickname: str):
    result = await new_horse(session.id1, name, nickname)
    await MessageUtils.build_message(result).finish(at_sender=True)


@_matcher.assign("my-horse")
async def _(session: EventSession, arparma: Arparma):
    result = await show_horse(session.id1)
    await MessageUtils.build_message(result).send(at_sender=True)

@_matcher.assign("rename-horse")
async def _(session: EventSession, arparma: Arparma, name: str, nickname: str):
    result = await rename_horse(session.id1, name, nickname)
    await MessageUtils.build_message(result).send(at_sender=True)


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
_matcher.shortcut(
    "1",
    command="赛马",
    arguments=["test1"],
    prefix=True,
)
_matcher.shortcut(
    "2",
    command="赛马",
    arguments=["test2"],
    prefix=True,
)
_matcher.shortcut(
    "3",
    command="赛马",
    arguments=["test3"],
    prefix=True,
)
_matcher.shortcut(
    "4",
    command="赛马",
    arguments=["test4"],
    prefix=True,
)
_matcher.shortcut(
    "5",
    command="赛马",
    arguments=["test5"],
    prefix=True,
)

@_matcher.assign("test1")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    pass
    user_id = session.id1
    await horse_getexp(user_id,430)
    await MessageUtils.build_message("测试指令，获取430经验").send()

@_matcher.assign("test2")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    pass
    user_id = session.id1
    horse = await get_horse(user_id)
    result = await horse_refresh_rate(horse)        #刷新属性

    await MessageUtils.build_message(result).send(at_sender=True)

@_matcher.assign("test3")
async def _(session: EventSession, arparma: Arparma, nickname: str = UserName()):
    pass
    a = [0, 1]
    result = a[0]
    await MessageUtils.build_message(str(result)).send(at_sender=True)
    result = a[2]
    await MessageUtils.build_message(str(result)).send(at_sender=True)

@_matcher.assign("test4")
async def _(session: EventSession, arparma: Arparma, level, a0, a1, a2, a3):
    pass
    result = await load_dlcs()
    await MessageUtils.build_message(str(result)).send(at_sender=True)

@_matcher.assign("test5")
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