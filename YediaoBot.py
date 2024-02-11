import botpy
from botpy.types.message import Message
from botpy.types.message import Reference
import requests
import pymysql
import mysql.connector
import multiprocessing
import aiomysql
import ast
import json

import time as Time
import asyncio
import re
import random
from decimal import *

fishing_state = {}
qh_state = {}

import requests
import re

def get_nick_name(num):
    url = f"https://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={num}"
    response = requests.get(url)
    data = response.text

    pattern = r'portraitCallBack\(\{"' + num + r'":\[".*?",\d+,-1,0,0,0,"(.*?)",0\]\}\)'
    match = re.search(pattern, data)
    
    if match:
        nick_name = match.group(1)
        return nick_name
    else:
        return None


def topphb(database, table, column, user_id, top_n):
    cnx = mysql.connector.connect(user='root', password='马赛克', host='马赛克', database=database)
    cursor = cnx.cursor()
    query = f"SELECT {column}, id FROM {table} ORDER BY CAST({column} AS UNSIGNED) DESC LIMIT {top_n}"
    cursor.execute(query)
    results = cursor.fetchall()
    user_rank = [i for i, x in enumerate(results) if x[1] == user_id]
    cnx.close()
    formatted_results = [f"Top{i+1}：<@!{result[1]}>：{result[0]}" for i, result in enumerate(results)]
    if user_rank:
        formatted_results.append(f"你的排行：第{user_rank[0] + 1}名")
    return "\n".join(formatted_results)



class MyClient(botpy.Client):
    async def on_message_create(self, message: Message):
        global fishing_state
        global qh_state
        botopenitem = 1
        if message.author.bot==True:
            return 0
        if message.author.id=="马赛克":#马赛克
            message.author.id="马赛克"
        if message.author.id=="马赛克":#马赛克
            message.author.id="马赛克"
        if message.author.id=="马赛克":#马赛克
            message.author.id="马赛克"
        if message.author.id=="马赛克":#马赛克
            message.author.id="马赛克"
        if message.author.id=="马赛克":#马赛克
            message.author.id="马赛克"
        if botopenitem == 1:

            #杂项
            等级 = Decimal(await data.read("属性",message.author.id,"等级","0"))
            经验 = Decimal(await data.read("属性",message.author.id,"经验","0"))
            经验需求 = ((Decimal("2")**min(等级,Decimal('10')))*(Decimal("1.1")**max(等级-Decimal('10'),0))*Decimal("100")).quantize(Decimal('0.'))
            if 经验>=经验需求:
                await data.write("属性", message.author.id, "等级",str(Decimal(await data.read("属性", message.author.id, "等级","0"))+1))
                等级+=1
                await data.write("属性", message.author.id, "经验","0")
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 恭喜升级！\n获得：天赋点*1\nLevel：{等级}',msg_id=message.message_id)
                await data.write("天赋", message.author.id, "天赋点",str(Decimal(await data.read("天赋", message.author.id, "天赋点","0"))+1))
            if re.match("测试", message.content) != None:
                time = Time.localtime(Time.time())
                if time[3]<=12:
                    time2 = '上午'
                else:
                    time2 = '下午'
                sfz = message.member.roles[0]
                if sfz == "11":
                    sfz = "成员"
                elif sfz == "2":
                    sfz = "管理员"
                elif sfz == "4":
                    sfz = "群主"
                elif sfz == "5":
                    sfz = "子频道管理员"
                await self.api.post_message(channel_id=message.channel_id, content=f'在呢<emoji:277>\r{sfz}{message.author.username}\r今天是{time[2]}\r{time2}0')
            elif re.match("开启宝箱", message.content) != None:
                author_id=message.author.id
                if await data.read("村庄_村民", author_id, "归属村庄","0") != "0":
                    village = await data.read("村庄_村民", author_id, "归属村庄","0")
                    if await data.read("村庄", village, "参加情况","0") != "0":
                        x = int(await data.read("村庄_村民", author_id, "村x",await data.read("村庄", village, "初始x","0")))
                        y = int(await data.read("村庄_村民", author_id, "村y",await data.read("村庄", village, "初始y","0")))
                        map = await data.read("四色战争地图", "0", "地块类型","0")
                        map = eval(map)
                        qu = map[x][y]
                        if qu=="资源":
                            vf = Decimal(await data.read("村庄_仓库",village,"鱼","0"))
                            vjf = Decimal(await data.read("数据",author_id,"鱼","0"))
                            vjf = vjf-all鱼+1 #什么报黄了 是BUG吗 不修了）
                            vf = vf+vjf
                            vf = str(vf)
                            await data.write("村庄_仓库",village,"鱼",vf)
                await self.api.post_message(channel_id=message.channel_id, content=f'开启失败！此处无宝箱')

            elif re.match(r"获取地块 ?([0-9]+) ([0-9]+)", message.content) != None:
                return 0
                x = int(re.match(r"获取地块 ?([0-9]+) ([0-9]+)", message.content).group(1))
                y = int(re.match(r"获取地块 ?([0-9]+) ([0-9]+)", message.content).group(2))
                y = 99-y
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                color = await data.read("村庄", color, "村庄名","0")
                map = await data.read("四色战争地图", "0", "地块食物","0")
                map = eval(map)
                food = map[x][y]
                map = await data.read("四色战争地图", "0", "总攻击","0")
                map = eval(map)
                k = map[x][y]
                map = await data.read("四色战争地图", "0", "总防御","0")
                map = eval(map)
                f = map[x][y]
                await self.api.post_message(channel_id=message.channel_id, content=f'地块类型：{qu}\n归属村庄：{color}\n剩余食物：{food}\n总攻击：{k}\n总防御：{f}')
            elif re.match(r"s([上下左右])", message.content) != None:
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                fx = re.match(r"s([上下左右])", message.content).group(1)
                if fx =="上":
                    xj = 0
                    yj = -1
                elif fx == "下":
                    xj = 0
                    yj = 1
                elif fx == "左":
                    xj = -1
                    yj = 0
                else:
                    xj = 1
                    yj = 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                x = x+xj
                y = y+yj
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                color = await data.read("村庄", color, "村庄名","0")
                map = await data.read("四色战争地图", "0", "地块食物","0")
                map = eval(map)
                food = map[x][y]
                map = await data.read("四色战争地图", "0", "总攻击","0")
                map = eval(map)
                k = map[x][y]
                map = await data.read("四色战争地图", "0", "总防御","0")
                map = eval(map)
                f = map[x][y]
                y = 99-y
                await self.api.post_message(channel_id=message.channel_id, content=f'前方坐标：x{x} y{y}\n地块类型：{qu}\n归属村庄：{color}\n剩余食物：{food}\n总攻击：{k}\n总防御：{f}')
            elif re.match(r"增兵 ?([0-9]+)", message.content) != None:
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                x = float(re.match(r"增兵 ?([0-9]+)", message.content).group(1))
                xd = float(await data.read("装备", message.author.id, "小刀","0"))
                if xd < x:
                    await self.api.post_message(channel_id=message.channel_id, content=f'你小刀不够')
                    return 0
                xd = xd-x
                await data.write("装备", message.author.id, "小刀",str(int(xd)))
                map = await data.read("四色战争地图", "0", "总攻击","0")
                map = eval(map)
                z = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                k = map[z][y]
                k = float(k)
                k = str(k+x)
                map[z][y]=k
                map =str(map)
                await data.write("四色战争地图", "0", "总攻击",map)
                await self.api.post_message(channel_id=message.channel_id, content=f'增兵成功！')
            elif re.match(r"收兵 ?([0-9]+)", message.content) != None:
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                x = float(re.match(r"收兵 ?([0-9]+)", message.content).group(1))
                xd = float(await data.read("装备", message.author.id, "小刀","0"))
                map = await data.read("四色战争地图", "0", "总攻击","0")
                map = eval(map)
                z = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                k = map[z][y]
                k = float(k)
                if x > k:
                    await self.api.post_message(channel_id=message.channel_id, content=f'此地兵力不够')
                    return 0
                xd = xd+x
                k = str(k-x)
                map[z][y]=k
                map =str(map)
                await data.write("四色战争地图", "0", "总攻击",map)
                xd = xd*0.8
                await data.write("装备", message.author.id, "小刀",str(int(xd)))
                await self.api.post_message(channel_id=message.channel_id, content=f'收兵成功！')
            elif re.match(r"设防 ?([0-9]+)", message.content) != None:
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                x = float(re.match(r"设防 ?([0-9]+)", message.content).group(1))
                xd = float(await data.read("装备", message.author.id, "头盔","0"))
                if xd < x:
                    await self.api.post_message(channel_id=message.channel_id, content=f'你头盔不够')
                    return 0
                xd = xd-x
                await data.write("装备", message.author.id, "头盔",str(int(xd)))
                map = await data.read("四色战争地图", "0", "总防御","0")
                map = eval(map)
                z = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                k = map[z][y]
                k = float(k)
                k = str(k+x)
                map[z][y]=k
                map =str(map)
                await data.write("四色战争地图", "0", "总防御",map)
                await self.api.post_message(channel_id=message.channel_id, content=f'设防成功！')
            elif message.content == "我的位置":
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "地块食物","0")
                map = eval(map)
                food = map[x][y]
                map = await data.read("四色战争地图", "0", "总攻击","0")
                map = eval(map)
                k = map[x][y]
                map = await data.read("四色战争地图", "0", "总防御","0")
                map = eval(map)
                f = map[x][y]
                x = str(x)
                y=99-y
                y = str(y)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> \n你的坐标是：x{x} y{y}\n地块类型：{qu}\n剩余食物：{food}\n总攻击：{k}\n总防御：{f}')
            elif message.content == "上":
                #不要喷我堆屎山（）做这个的时候很赶时间（）
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                y = y-1
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                if y==-1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你在地图最上面')
                    return 0
                if qu=="禁区" or qu=="怪物":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方有怪物，请输入：攻击上')
                    return 0
                if color !="0" and color !=village:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方为敌军区域，请输入：攻击上')
                    return 0
                y=str(y)
                await data.write("村庄_村民", message.author.id, "村y",y)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 移动成功！')
            elif message.content == "下":
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                y = y+1
                if y==100:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你在地图最下面')
                    return 0
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                if qu=="禁区" or qu=="怪物":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方有怪物，请输入：攻击下')
                    return 0
                if color !="0" and color !=village:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方为敌军区域，请输入：攻击下')
                    return 0
                y=str(y)
                await data.write("村庄_村民", message.author.id, "村y",y)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 移动成功！')
            elif message.content == "左":
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                x = x-1
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                if x==-1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你在地图最左面')
                    return 0
                if qu=="禁区" or qu=="怪物":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方有怪物，请输入：攻击左')
                    return 0
                if color !="0" and color !=village:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方为敌军区域，请输入：攻击左')
                    return 0
                x=str(x)
                await data.write("村庄_村民", message.author.id, "村x",x)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 移动成功！')
            elif message.content == "右":
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                x = x+1
                if x==100:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你在地图最右面')
                    return 0
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                if qu=="禁区" or qu=="怪物":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方有怪物，请输入：攻击右')
                    return 0
                if color !="0" and color !=village:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方为敌军区域，请输入：攻击右')
                    return 0
                x=str(x)
                await data.write("村庄_村民", message.author.id, "村x",x)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 移动成功！')
            elif message.content == "占领地块":
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                if color ==village:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 这已经是你村地盘了')
                    return 0
                fish = Decimal(await data.read("数据",message.author.id,"鱼","0"))
                if fish<1000:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你需要1000条鱼来占领此地')
                    return 0
                fish = fish-1000
                await data.write("数据",message.author.id,"鱼",str(fish))
                map = await data.read("四色战争地图", "0", "地块食物","0")
                map = eval(map)
                food = int(map[x][y])
                food = str(food+1000)
                map[x][y]=food
                map = str(map)
                await data.write("四色战争地图", "0", "地块食物",map)
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                map[x][y] = village
                map = str(map)
                await data.write("四色战争地图", "0", "村庄归属",map)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 占领成功！')
            elif re.match(r"攻击([上下左右])",message.content) != None:
                fx = re.match(r"攻击([上下左右])", message.content).group(1)
                if fx =="上":
                    xj = 0
                    yj = -1
                elif fx == "下":
                    xj = 0
                    yj =1
                elif fx == "左":
                    xj = -1
                    yj = 0
                else:
                    xj = 1
                    yj = 0
                if await data.read("村庄_村民", message.author.id, "归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有加入任何村庄')
                    return 0
                village = await data.read("村庄_村民", message.author.id, "归属村庄","0")
                if await data.read("村庄", village, "参加情况","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你村庄没有参加四色战争')
                    return 0
                x = int(await data.read("村庄_村民", message.author.id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", message.author.id, "村y",await data.read("村庄", village, "初始y","0")))
                x = x+xj
                y = y+yj
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                map = await data.read("四色战争地图", "0", "村庄归属","0")
                map = eval(map)
                color = map[x][y]
                if y==-1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你在地图最上面')
                    return 0
                if qu=="禁区" or qu=="怪物":
                    map = await data.read("四色战争地图", "0", "总防御","0")
                    map = eval(map)
                    yst = map[x][y]
                    yst = float(yst)
                    if yst < 1 and qu =="禁区":
                        csh = random.uniform(1500, 2300)
                        csh = str(csh)
                        map[x][y]=csh
                        map = str(map)
                        await data.write("四色战争地图", "0", "总防御",map)
                    if yst < 1 and qu =="怪物":
                        csh = random.uniform(300, 500)
                        csh = str(csh)
                        map[x][y]=csh
                        map = str(map)
                        await data.write("四色战争地图", "0", "总防御",map)
                elif color !="0" and color !=village:
                    pass
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 前方不需要攻击')
                    return 0
                map = await data.read("四色战争地图", "0", "总防御","0")
                map = eval(map)
                yst = map[x][y]
                yst = float(yst)
                x = x-xj
                y = y-yj
                map = await data.read("四色战争地图", "0", "总攻击","0")
                map = eval(map)
                mst = map[x][y]
                mst = float(mst)
                luck = random.uniform(0.9, 1.1)
                ls1 = yst*luck
                luck = random.uniform(0.9, 1.1)
                ls2 = mst*luck
                win = 0
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 攻击中.....\n对局：1/3')
                print ("1")
                sleep_time = random.randint(5,10)
                print ("2")
                await asyncio.sleep(sleep_time)
                print ("3")
                if ls2 > ls1:
                    win = win+1
                    win = str(win)
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 攻击成功！正在进行下一轮攻击......\n对局：2/{win}/3')
                    win = int(win)
                    sleep_time = random.randint(5,10)
                    await asyncio.sleep(sleep_time)
                else:
                    win = str(win)
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 攻击失败！正在进行下一轮攻击......\n对局：2/{win}/3')
                    win = int(win)
                    sleep_time = random.randint(5,10)
                    await asyncio.sleep(sleep_time)
                luck = random.uniform(0.9, 1.1)
                ls1 = yst*luck
                luck = random.uniform(0.9, 1.1)
                ls2 = mst*luck
                if ls2 > ls1:
                    win = win+1
                    win = str(win)
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 攻击成功！正在进行下一轮攻击......\n对局：3/{win}/3')
                    win = int(win)
                    sleep_time = random.randint(5,10)
                    await asyncio.sleep(sleep_time)
                else:
                    win = str(win)
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 攻击失败！正在进行下一轮攻击......\n对局：3/{win}/3')
                    win = int(win)
                    sleep_time = random.randint(5,10)
                    await asyncio.sleep(sleep_time)
                luck = random.uniform(0.9, 1.1)
                ls1 = yst*luck
                luck = random.uniform(0.9, 1.1)
                ls2 = mst*luck
                if ls2 > ls1:
                    win = win+1
                else:
                    pass
                if win >=2:
                    x = x+xj
                    y = y+yj
                    mapc = await data.read("四色战争地图", "0", "地块类型","0")
                    mapc = eval(mapc)
                    qu = mapc[x][y]
                    map = await data.read("四色战争地图", "0", "村庄归属","0")
                    map = eval(map)
                    color = map[x][y]
                    mapa=await data.read("四色战争地图", "0", "总攻击","0")
                    mapa = eval(mapa)
                    luck = random.uniform(0.7, 0.9)
                    ss = yst*luck
                    mst = mst-yst
                    mst = str(mst)
                    mapa[x-xj][y-yj]=mst
                    mapa = str(mapa)
                    await data.write("四色战争地图", "0", "总攻击",mapa)
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 攻击成功！前方地块已变为无主状态\n战损：{ss}')
                    await data.write("四色战争地图", "0", "总攻击",mapa)
                    if qu=="怪物":
                        qu = "空白"
                        mapc[x][y]=qu
                        mapc = str(mapc)
                        await data.write("四色战争地图", "0", "地块类型",mapc)
                    elif qu=="禁区":
                        qu="资源"
                        mapc[x][y]=qu
                        mapc = str(mapc)
                        await data.write("四色战争地图", "0", "地块类型",mapc)
                    else:
                        map[x][y]="0"
                        map = str(map)
                        await data.write("四色战争地图", "0", "村庄归属",map)
                else:
                    luck = random.uniform(0.3, 0.6)
                    ss = mst*luck
                    mst = mst-ss
                    mst = str(mst)
                    map[x][y]=mst
                    map = str(map)
                    await data.write("四色战争地图", "0", "总攻击",map)
                    ss = str(ss)
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 攻击失败！损失{ss}兵力！')
                
                
                



            elif message.content == "领取补偿":
                if await data.read("其他",message.author.id,"补偿","0") == "1":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经领取过了111')
                else:
                    银行斯玛特 = Decimal(await data.read("货币",message.author.id,"银行斯玛特","0"))
                    add_银行斯玛特 = (Decimal("2")*银行斯玛特).quantize(Decimal("0."))
                    await data.write("其他",message.author.id,"补偿","1")
                    await data.write("货币",message.author.id,"银行斯玛特",str(add_银行斯玛特))
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 领取成功！获得{银行斯玛特}斯玛特！已自动存入')
            if message.content=='我的ID':
                await self.api.post_message(channel_id=message.channel_id, content=f'{message.author.id}')
            if message.content=='getid':
                await self.api.post_message(channel_id=message.channel_id, content=f'{message.author.id}')
            elif re.match("获取ID<@![0-9]+>", message.content) != None:
                user_id = int(message.mentions[0].id)
                await self.api.post_message(channel_id=message.channel_id, content=f'{user_id}')
            elif re.match("强制转移([0-9]+)<@![0-9]+>", message.content) != None:
                if message.author.id == "11782375117980851014":
                    iidd = str(message.mentions[0].id)
                    num = re.search("[0-9]+", message.content).group()
                    await self.api.post_message(channel_id=message.channel_id, content='验证成功！请等待更新。\r在更新完成时，将会通知你\r在此之前不要进行任何操作')
                    await data.write("货币", iidd, "银行斯玛特",await data.read("oldfisher",num,"银行余额","0"))
                    await data.write("货币", iidd, "斯玛特",await data.read("oldfisher",num,"斯玛特","0"))
                    await data.write("属性", iidd, "体力上限", int(await data.read("oldfisher",num,"体力上限","100")) + 100)
                    await data.write("属性", iidd, "精力上限", int(await data.read("oldfisher",num,"精力上限","100")) + 100)
                    await data.write("装备", iidd, "鱼竿",await data.read("oldfisher",num,"鱼竿等级","0"))
                    await data.write("装备", iidd, "小刀",await data.read("oldfisher",num,"小刀等级","0"))
                    await data.write("装备", iidd, "头盔",await data.read("oldfisher",num,"头盔等级","0"))
                    await data.write("装备", iidd, "钱袋",await data.read("oldfisher",num,"钱袋等级","0"))
                    await data.write("装备", iidd, "韧线",await data.read("oldfisher",num,"韧线等级","0"))
                    await data.write("其他", iidd, "属性礼包1",await data.read("oldfisher",num,"属性礼包1","0"))
                    await data.write("其他", iidd, "属性礼包2",await data.read("oldfisher",num,"属性礼包2","0"))
                    await data.write("装备", iidd, "咖啡帽",await data.read("oldfisher",num,"咖啡帽","0"))
                    await data.write("装备", iidd, "大容量水壶",await data.read("oldfisher",num,"大容量水壶","0"))
                    await data.write("装备", iidd, "军用铲子",await data.read("oldfisher",num,"军用铲子","0"))
                    await data.write("装备", iidd, "上古农书",await data.read("oldfisher",num,"上古农书","0"))
                    await data.write("装备", iidd, "鱼吸引器",await data.read("oldfisher",num,"鱼吸引器","0"))
                    await data.write("装备", iidd, "多功能锄",await data.read("oldfisher",num,"多功能锄","0"))
                    await data.write("装备", iidd, "RPG",await data.read("oldfisher",num,"RPG","0"))
                    await data.write("物品", iidd, "兑换券",await data.read("oldfisher",num,"预约兑换券","0"))
                    #await data.write("属性", iidd, "专属头衔",await data.read("oldfisher",num,"专属头衔","0"))
                    await data.write("属性", iidd, "等级",await data.read("oldfisher",num,"等级","0"))
                    await data.write("属性", iidd, "经验",await data.read("oldfisher",num,"经验","0"))
                    await data.write("装备", iidd, "渔网",await data.read("oldfisher",num,"渔网","0"))
                    await data.write("货币", iidd, "农场币",await data.read("oldfisher",num,"农场币","0"))
                    await data.write("天赋", iidd, "经验天赋1",await data.read("oldfisher",num,"经验天赋1","0"))
                    await data.write("天赋", iidd, "渔民天赋1",await data.read("oldfisher",num,"渔民天赋1","0"))
                    await data.write("天赋", iidd, "渔民天赋2",await data.read("oldfisher",num,"渔民天赋2","0"))
                    await data.write("天赋", iidd, "天赋点",await data.read("oldfisher",num,"天赋点","0"))
                    await data.write("其他", iidd, "状态","1")
                    await data.write("其他", iidd, "验证码","HHHHHHHHHH")
                    await data.write("其他",num,"状态","1")
                    await self.api.post_message(channel_id=message.channel_id, content='更新完成！')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content='你没有权限')
            elif re.match("转移账号([0-9]+)", message.content) != None:
                yzma = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=10))
                num = re.search("[0-9]+", message.content).group()
                yzm = await data.read("其他", message.author.id, "验证码", {yzma})
                nick_name = get_nick_name(num)
                if await data.read("其他", message.author.id, "状态", '0') == '1':
                    await self.api.post_message(channel_id=message.channel_id, content='你的账号已经转移过了')
                elif await data.read("其他", num, "状态", '0') == '1':
                    await self.api.post_message(channel_id=message.channel_id, content='此QQ号已被转移')
                elif nick_name == yzm:
                    await self.api.post_message(channel_id=message.channel_id, content='验证成功！请等待更新。\r在更新完成时，将会通知你\r在此之前不要进行任何操作')
                    iidd = str(message.author.id)
                    await data.write("货币", iidd, "银行斯玛特",await data.read("oldfisher",num,"银行余额","0"))
                    await data.write("货币", iidd, "斯玛特",await data.read("oldfisher",num,"斯玛特","0"))
                    await data.write("属性", iidd, "体力上限", int(await data.read("oldfisher",num,"体力上限","100")) + 100)
                    await data.write("属性", iidd, "体力上限", int(await data.read("oldfisher",num,"精力上限","100")) + 100)
                    await data.write("装备", iidd, "鱼竿",await data.read("oldfisher",num,"鱼竿等级","0"))
                    await data.write("装备", iidd, "小刀",await data.read("oldfisher",num,"小刀等级","0"))
                    await data.write("装备", iidd, "头盔",await data.read("oldfisher",num,"头盔等级","0"))
                    await data.write("装备", iidd, "钱袋",await data.read("oldfisher",num,"钱袋等级","0"))
                    await data.write("装备", iidd, "韧线",await data.read("oldfisher",num,"韧线等级","0"))
                    await data.write("其他", iidd, "属性礼包1",await data.read("oldfisher",num,"属性礼包1","0"))
                    await data.write("其他", iidd, "属性礼包2",await data.read("oldfisher",num,"属性礼包2","0"))
                    await data.write("装备", iidd, "咖啡帽",await data.read("oldfisher",num,"咖啡帽","0"))
                    await data.write("装备", iidd, "大容量水壶",await data.read("oldfisher",num,"大容量水壶","0"))
                    await data.write("装备", iidd, "军用铲子",await data.read("oldfisher",num,"军用铲子","0"))
                    await data.write("装备", iidd, "上古农书",await data.read("oldfisher",num,"上古农书","0"))
                    await data.write("装备", iidd, "鱼吸引器",await data.read("oldfisher",num,"鱼吸引器","0"))
                    await data.write("装备", iidd, "多功能锄",await data.read("oldfisher",num,"多功能锄","0"))
                    await data.write("装备", iidd, "RPG",await data.read("oldfisher",num,"RPG","0"))
                    await data.write("物品", iidd, "兑换券",await data.read("oldfisher",num,"预约兑换券","0"))
                    #await data.write("属性", iidd, "专属头衔",await data.read("oldfisher",num,"专属头衔","0"))
                    await data.write("属性", iidd, "等级",await data.read("oldfisher",num,"等级","0"))
                    await data.write("属性", iidd, "经验",await data.read("oldfisher",num,"经验","0"))
                    await data.write("装备", iidd, "渔网",await data.read("oldfisher",num,"渔网","0"))
                    await data.write("货币", iidd, "农场币",await data.read("oldfisher",num,"农场币","0"))
                    await data.write("天赋", iidd, "经验天赋1",await data.read("oldfisher",num,"经验天赋1","0"))
                    await data.write("天赋", iidd, "渔民天赋1",await data.read("oldfisher",num,"渔民天赋1","0"))
                    await data.write("天赋", iidd, "渔民天赋2",await data.read("oldfisher",num,"渔民天赋2","0"))
                    await data.write("天赋", iidd, "天赋点",await data.read("oldfisher",num,"天赋点","0"))
                    await data.write("其他", iidd, "状态","1")
                    await data.write("其他",num,"状态","1")
                    await self.api.post_message(channel_id=message.channel_id, content='更新完成！')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'{nick_name}请修改QQ昵称为“{yzm}”以验证身份')
            elif re.match("排行榜", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content='''┌选择排行榜
├─────
├🏘️村钓赛🏘️
├村庄贡献排行
├等级排行
├钓鱼排行
├农场币排行
├鱼竿排行
├韧线排行
├渔网排行
├小刀/头盔/钱袋排行
├富豪榜（现金）
└─────
注：排行榜只展示前五名''')
            elif re.match("村钓赛", message.content) != None:
                iidd = await data.read("村庄_村民",message.author.id,"归属村庄","0")
                await self.api.post_message(channel_id=message.channel_id, content=f'🏘️村钓赛🏘️\n{await data.topcds("fisher", "村庄", "钓鱼次数", iidd, 5)}')
            elif re.match("钓鱼排行", message.content) != None:
                iidd = await data.read("村庄_村民",message.author.id,"归属村庄","0")
                await self.api.post_message(channel_id=message.channel_id, content=f'🎣钓鱼排行🎣\n{topphb("fisher", "数据", "钓鱼次数", message.channel_id, 5)}')
            elif re.match("富豪榜", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'💰富豪榜💰\n{topphb("fisher", "货币", "斯玛特", message.channel_id, 5)}')
            elif re.match("鱼竿排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'🎣鱼竿排行🎣\n{topphb("fisher", "装备", "鱼竿", message.channel_id, 5)}')
            elif re.match("韧线排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'🎣韧线排行🎣\n{topphb("fisher", "装备", "韧线", message.channel_id, 5)}')
            elif re.match("渔网排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'🎣渔网排行🎣\n{topphb("fisher", "装备", "渔网", message.channel_id, 5)}')
            elif re.match("小刀排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'🔪小刀排行🔪\n{topphb("fisher", "装备", "小刀", message.channel_id, 5)}')
            elif re.match("头盔排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'⛑️头盔排行⛑️\n{topphb("fisher", "装备", "头盔", message.channel_id, 5)}')
            elif re.match("钱袋排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'💰钱袋排行💰\n{topphb("fisher", "装备", "钱袋", message.channel_id, 5)}')
            elif re.match("农场币排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'🌾农场币排行🌾\n{topphb("fisher", "货币", "农场币", message.channel_id, 5)}')
            elif re.match("等级排行", message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content=f'🆒等级排行🆒\n{topphb("fisher", "属性", "等级", message.channel_id, 5)}')
            elif message.content=='菜单':
                await self.api.post_message(channel_id=message.channel_id, content='''🧑我的属性|💰寻宝
🏦银行|💰打劫
🏪商店|🎣钓鱼
☕️休息|📆签到
🏠家园|🏆排行
🚜农场|💴活动
🧑名片|🏠村庄
一些指令用法：
转账@对象 钱数
打劫@对象''')

            elif message.content=='我的属性':
                sfz = message.member.roles[0]
                if sfz == "11":
                    sfz = "普通成员"
                elif sfz == "2":
                    sfz = "管理员"
                elif sfz == "4":
                    sfz = "群主"
                elif sfz == "5":
                    sfz = "子频道管理员"
                体力 = Decimal(await data.read("属性",message.author.id,"体力","100"))
                体力上限 = Decimal(await data.read("属性",message.author.id,"体力上限","100"))
                精力 = Decimal(await data.read("属性",message.author.id,"精力","100"))
                精力上限 = Decimal(await data.read("属性",message.author.id,"精力上限","100"))
                等级 = Decimal(await data.read("属性",message.author.id,"等级","0"))
                经验 = Decimal(await data.read("属性",message.author.id,"经验","0"))
                经验需求 = ((Decimal("2")**min(等级,Decimal('10')))*(Decimal("1.1")**max(等级-Decimal('10'),0))*Decimal("100")).quantize(Decimal('0.'))
                await self.api.post_message(channel_id=message.channel_id, content=f'''【{sfz}】{message.author.username}
财富头衔：{await data.read("属性",message.author.id,"财富头衔","0")}
专属头衔：{await data.read("属性",message.author.id,"专属头衔","0")}
Level：{等级}
EXP：{经验}/{经验需求}
樱桃币：{await data.read("物品",message.author.id,"樱桃币","0")}
斯玛特：{await data.read("货币",message.author.id,"斯玛特","0")}
农场币：{await data.read("货币",message.author.id,"农场币","20")}
寻宝券：{await data.read("物品",message.author.id,"寻宝券","0")}
兑换券：{await data.read("物品",message.author.id,"兑换券","0")}
体力：{体力}/{体力上限}({(体力/体力上限*Decimal("100")).quantize(Decimal('0.00'))}%)
精力：{精力}/{精力上限}({(精力/精力上限*Decimal("100")).quantize(Decimal('0.00'))}%)
「其他物品」
鱼饵：{await data.read("物品",message.author.id,"鱼饵","0")}
鱼：{await data.read("数据",message.author.id,"鱼","0")}
「特殊物品」
输入"物品栏"查看''')

            elif message.content=='物品栏':
                msg = message.author.username + '的物品栏'
                鱼竿 = Decimal(await data.read("装备",message.author.id,"鱼竿","0"))
                韧线 = await data.read("装备",message.author.id,"韧线","0")
                渔网 = await data.read("装备",message.author.id,"渔网","0")
                小刀 = await data.read("装备",message.author.id,"小刀","0")
                头盔 = await data.read("装备",message.author.id,"头盔","0")
                钱袋 = await data.read("装备",message.author.id,"钱袋","0")
                附魔 = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                破限石 = await data.read("物品",message.author.id,"破限石","0")
                if 鱼竿 > 9:
                    msg = msg + '\r' + '9级鱼竿+' + str(鱼竿 - 9) + 附魔
                if 鱼竿 > 0 and 鱼竿 <= 9:
                    msg = msg + '\r'  + str(鱼竿) + '级鱼竿' + 附魔
                if 韧线 != "0":
                    msg = msg + '\r' + 韧线 + '级韧线'
                if 渔网 != "0":
                    msg = msg + '\r' + 渔网 + '级渔网'
                if 小刀 != "0":
                    msg = msg + '\r' + 小刀 + '级小刀'
                if 头盔 != "0":
                    msg = msg + '\r' + 头盔 + '级头盔'
                if 钱袋 != "0":
                    msg = msg + '\r' + 钱袋 + '级钱袋'
                if await data.read("装备",message.author.id,"咖啡帽","0") != "0":
                    msg = msg + '\r' + '咖啡帽'
                if await data.read("装备",message.author.id,"大容量水壶","0") != "0":
                    msg = msg + '\r' + '大容量水壶'
                if await data.read("装备",message.author.id,"军用铲子","0") != "0":
                    msg = msg + '\r' + '军用铲子'
                if await data.read("装备",message.author.id,"上古农书","0") != "0":
                    msg = msg + '\r' + '上古农书'
                if await data.read("装备",message.author.id,"多功能锄","0") != "0":
                    msg = msg + '\r' + '多功能锄'
                鱼吸 = await data.read("装备",message.author.id,"鱼吸引器","0")
                鱼吸列表 = {"1":"鱼吸引器","2":"声呐"}
                if 鱼吸 != "0":
                    msg = msg + '\r' + 鱼吸列表[鱼吸]
                if await data.read("装备",message.author.id,"RPG","0") != "0":
                    msg = msg + '\r' + 'RPG'
                戒指 = await data.read("装备",message.author.id,"戒指","0")
                戒指列表 = {"1":"镀金戒指","2":"黄金戒指","3":"钻石戒指","4":"红宝石戒指"}
                if 戒指 != "0":
                    msg = msg + '\r' + 戒指列表[戒指]
                if 破限石 != "0":
                    msg = msg + '\r' + '破限石*' + 破限石
                msg = msg + '\r' + "附魔书（对应着看）：" + '\r' + await data.read("物品",message.author.id,"附魔书","[['空书'],['0']]")
                await self.api.post_message(channel_id=message.channel_id, content=msg)

            elif message.content == '钓鱼' or message.content == '抛竿' or message.content == '抛杆':
                GodA = await data.read("其他",message.author.id,"赫拉克勒斯","0")
                try:
                    fish_state = fishing_state[message.author.id]
                except:
                    fish_state = 0
                if fish_state == 1 or fish_state == 2:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经在钓鱼啦！')
                else:
                    鱼饵 = Decimal(await data.read("物品",message.author.id,"鱼饵","0"))
                    体力 = Decimal(await data.read("属性",message.author.id,"体力","100"))
                    精力 = Decimal(await data.read("属性",message.author.id,"精力","100"))
                    if 鱼饵 == 0:
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 鱼饵不足\r输入"钓鱼商店"查看详情')
                        return 0
                    if 体力 < 5 and GodA !=1:
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 体力不支')
                        return 0
                    if 精力 < 1 and GodA !=1:
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 精力不支')
                        return 0
                    await data.write("物品",message.author.id,"鱼饵",str(鱼饵-Decimal("1")))
                    if GodA !="1":
                        await data.write("属性",message.author.id,"体力",str(体力-Decimal("5")))
                        await data.write("属性",message.author.id,"精力",str(精力-Decimal("1")))
                    fishing_state[message.author.id] = 1
                    if GodA !="1":
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 抛出鱼竿……\r剩余鱼饵：{鱼饵-Decimal(1)}\r剩余体力：{体力-Decimal("5")}\r剩余精力：{精力-Decimal("1")}\r[等待上钩]')
                    else:
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 抛出鱼竿……\r剩余鱼饵：{鱼饵-Decimal(1)}\r附魔技能[赫拉克勒斯]发动：\r钓鱼时不消耗体力和精力\r[等待上钩]')
                    sleep_time = random.randint(10000,25000)/1000
                    鱼吸 = await data.read("装备",message.author.id,"鱼吸引器","0")
                    sleep_time = sleep_time / 1.5
                    if 鱼吸 == "1":
                        sleep_time = sleep_time / 1.2
                    if 鱼吸 == "2":
                        sleep_time = sleep_time / 1.5
                    if Decimal(await data.read("装备",message.author.id,"鱼竿","0")) >=1000:
                        sleep_time = sleep_time / 1.5
                    if Decimal(await data.read("装备",message.author.id,"渔网","0")) >=10:
                        sleep_time = sleep_time / 1.5
                    #附魔效果开始
                    fm = "海之厌恶"
                    yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                    level =yfm.find(fm)
                    if level !=-1:
                        level = int(yfm[level + len(fm)])
                        fmxg = eval(await data.read("附魔",fm,"各级效果","0"))
                        print(fmxg)
                        fmxg = Decimal(fmxg[level-1])
                        fmxg = fmxg/100
                        print(level)
                        print(fmxg)
                        sleep_time = sleep_time*(1+fmxg)

                    fm = "海洋之息"
                    yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                    level =yfm.find(fm)
                    if level !=-1:
                        level = int(yfm[level + len(fm)])
                        fmxg = eval(await data.read("附魔",fm,"各级效果","0"))
                        print(fmxg)
                        fmxg = float(fmxg[level-1])
                        fmxg = fmxg/100
                        print(level)
                        print(fmxg)
                        sleep_time = sleep_time/(1+fmxg)

                    fm = "戒律·深罪之槛"
                    yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                    level =yfm.find(fm)
                    if level !=-1:
                        sleep_time = sleep_time*3
                    
                    fm = "黄金·璀璨之歌"
                    yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                    level =yfm.find(fm)
                    if level !=-1:
                        sleep_time = sleep_time*3
                    
                    fm = "繁星·绘世之卷"
                    yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                    level =yfm.find(fm)
                    if level !=-1:
                        sleep_time = sleep_time*3
                    #附魔效果结束
                    await asyncio.sleep(sleep_time)
                    if fishing_state[message.author.id] == 1:
                        fishing_state[message.author.id] = 2
                        await self.api.post_message(channel_id=message.channel_id, content=f'鱼上钩了！<@!{message.author.id}> 快拉竿！')
                    sleep_time = random.randint(2200,4000)/1000
                    await asyncio.sleep(sleep_time)
                    韧线 = Decimal(await data.read("装备",message.author.id,"韧线","0"))
                    while 1:
                        if random.randint(0,3) < 韧线 and fishing_state[message.author.id] == 2:  
                            await asyncio.sleep(0.6)
                        else:
                            break
                    if fishing_state[message.author.id] == 2:
                        fishing_state[message.author.id] = 3
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 鱼跑掉了......')

            elif re.match("[拉收][竿杆]",message.content) != None:
                try:
                    fish_state = fishing_state[message.author.id]
                except:
                    fish_state = 0
                fishing_state[message.author.id] = 0
                if fish_state == 0:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 还没有抛竿呢，睡迷糊了吗？')
                    return 0
                if fish_state == 1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你提前收竿，什么也没得到')
                    return 0
                if fish_state == 3:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 拉竿太晚……鱼跑掉了')
                    return 0
                体力 = Decimal(await data.read("属性",message.author.id,"体力","100"))
                sub_体力 = Decimal(str(random.randint(1,3)))
                GodA = await data.read("其他",message.author.id,"赫拉克勒斯","0")
                if 体力 < sub_体力 and GodA !="1":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 体力不足拉竿！')
                    return 0
                if GodA !="1":
                    await data.write("属性",message.author.id,"体力",str(体力-sub_体力))
                msg = f"<@!{message.author.id}> 钓到了："
                GodA = await data.read("其他",message.author.id,"量子之海","0")
                if GodA == "1":
                    msg += "\r「量子之海 · 附魔发动」所有收益*2"
                fm = "戒律·深罪之槛"
                yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                level =yfm.find(fm)
                if level !=-1:
                    msg += "\r「戒律·深罪之槛 · 附魔发动」钓鱼时间延长收益增多"
                    
                fm = "黄金·璀璨之歌"
                yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                level =yfm.find(fm)
                if level !=-1:
                    msg += "\r「黄金·璀璨之歌 · 附魔发动」钓鱼时间延长收益增多"
                    
                fm = "繁星·绘世之卷"
                yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                level =yfm.find(fm)
                if level !=-1:
                    msg += "\r「繁星·绘世之卷 · 附魔发动」钓鱼时间延长收益增多"
                msg += "\r「普通钓鱼」" + await self.上钩(message.author.id)
                鱼竿 = Decimal(await data.read("装备",message.author.id,"鱼竿","0"))
                #附魔效果开始
                fm = "饵钓"
                yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                level =yfm.find(fm)
                if level !=-1:
                    level = int(yfm[level + len(fm)])
                    fmxg = eval(await data.read("附魔",fm,"各级效果","0"))
                    print(fmxg)
                    fmxg = int(fmxg[level-1])
                    print(level)
                    print(fmxg)
                else:
                    fmxg = -1
                #附魔效果结束
                if random.randint(0,99)<20*min(鱼竿-8,1)+max(鱼竿-9,0)*2:
                    msg += "\r「鱼竿技能」" + await self.上钩(message.author.id)
                if random.randint(0,99)<10*int(await data.read("装备",message.author.id,"渔网","0")):
                    msg += "\r「渔网技能」" + await self.上钩(message.author.id)
                if random.randint(0,99)<10*int(await data.read("天赋",message.author.id,"渔民天赋1","0")):
                    msg += "\r「天赋技能」" + await self.上钩(message.author.id)
                if random.randint(0,99)<int(fmxg):
                    msg += "\r「附魔技能」" + await self.上钩(message.author.id)
                await self.api.post_message(channel_id=message.channel_id, content=msg)

            elif message.content == "休息":
                time = Time.localtime(Time.time())
                time_xiuxi = await data.read("其他",message.author.id,"休息","0-0.0")
                xiuxi = re.search("\.([0-9]+)",time_xiuxi).group()
                xiuxi = int(re.search("([0-9]+)",xiuxi).group())
                xiuxi2 = re.match("([0-9]+)-([0-9]+)",time_xiuxi).group()
                if xiuxi2 == f"{str(time[7])}" and (xiuxi/13)//1 == (time[3]/13)//1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 您还不累呢~')
                else:
                    msg1 = await data.属性操作(message.author.id,"精力",str(random.randint(40,80)),"add")
                    msg2 = await data.属性操作(message.author.id,"体力",str(random.randint(50,100)),"add")
                    await data.write("其他",message.author.id,"休息",f"{str(time[7])}.{str(time[3])}")
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 休息成功\r{msg1}\t{msg2}')

            elif re.match(r"天赋加点 ?(.*)",message.content) != None:
                block = re.match(r"天赋加点 ?(.*)",message.content).group(1)
                tf = await data.read("天赋",block,"block","0")
                if tf == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 不存在此天赋')
                    return 0
                level = int(await data.read("天赋",message.author.id,block,"0"))
                if level >=10:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{block}】已达满级，无法再进一步')
                    return 0
                point = int(await data.read("天赋",message.author.id,"天赋点","0"))
                if level >7:
                    cost = 2
                else:
                    cost = 1
                if point < cost:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 天赋点不足！{point}/{cost}')
                    return 0
                point = str(point - cost)
                level = str(level + 1)
                await data.write("天赋",message.author.id,block,level)
                await data.write("天赋",message.author.id,"天赋点",point)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{block}】升级成功！')

            elif re.match(r"天赋遗忘 ?(.*)",message.content) != None:
                block = re.match(r"天赋遗忘 ?(.*)",message.content).group(1)
                tf = await data.read("天赋",block,"block","0")
                if tf == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 不存在此天赋')
                    return 0
                level = int(await data.read("天赋",message.author.id,block,"0"))
                if level <=0:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你还没有掌握【{block}】')
                    return 0
                point = int(await data.read("天赋",message.author.id,"天赋点","0"))
                if level >8:
                    cost = 2
                else:
                    cost = 1
                point = str(point + cost)
                level = str(level - 1)
                await data.write("天赋",message.author.id,block,level)
                await data.write("天赋",message.author.id,"天赋点",point)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{block}】遗忘了一部分......')

            elif message.content == "天赋大全":
                await self.api.post_message(channel_id=message.channel_id, content=f'''【渔民天赋】
【经验天赋】
天赋加点指令：天赋加点+天赋名''')
            elif message.content == "经验天赋":
                level = Decimal(await data.read("天赋",message.author.id,"经验天赋1","0"))
                more = level*50
                cost = (level-(level%8))/8+1
                await self.api.post_message(channel_id=message.channel_id, content=f'''经验天赋1({level}/10)
效果：经验获取增加{more}%
升级需求：{cost}天赋点''')
                
            elif message.content == "渔民天赋":
                level = Decimal(await data.read("天赋",message.author.id,"渔民天赋1","0"))
                more = level*10
                cost = (level-(level%8))/8+1
                level2 = Decimal(await data.read("天赋",message.author.id,"渔民天赋2","0"))
                more2 = level2*5
                cost2 = (level2-(level2%8))/8+1
                await self.api.post_message(channel_id=message.channel_id, content=f'''渔民天赋1({level}/10)
效果：钓鱼时有{more}%的几率额外钓上一条鱼
升级需求：{cost}天赋点
渔民天赋2({level2}/10)
效果：钓鱼时有{more2}%的几率钓上鱼王，鱼王的收益为普通鱼的2倍，EXP是普通鱼的5倍
升级需求：{cost2}天赋点''')

            elif message.content == "寻宝":
                #总而言之，言而总之，懒(lan，第三声)
                print("")

            #附魔主体
            elif re.match(r"祛魔 ?鱼竿 ?(.*)", message.content) != None:
                fm = re.match(r"祛魔 ?鱼竿 ?(.*)", message.content).group(1)
                yfm = await data.read("装备", message.author.id, "鱼竿附魔", "[]")
                yfm = yfm.replace("'", "")
                yfm = yfm.replace(" ", "")
                print(yfm)
                book = await data.read("物品", message.author.id, "附魔书", "[['空书'],['0']]")
                book = eval(book)
                level = re.findall(r'\d+', fm)
                if "空书" in book[0]:
                    row = book[0].index("空书")
                    value = int(book[1][row])
                else:
                    book[0].append("空书")
                    book[1].append("0")
                    value = 0
                if fm in book[0]:
                    underline = book[0].index(fm)
                else:
                    book[0].append(fm)
                    book[1].append("0")
                    underline = book[0].index(fm)
                if fm not in yfm:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你还没有这个附魔')
                    return 0
                yfm = yfm.strip("[]").split(",")
                cost_money = 1000000 * int(level[0]) * len(yfm)
                cost_exp = 100 * int(level[0]) * len(yfm)
                if Decimal(await data.read("货币", message.author.id, "斯玛特", "0")) < cost_money:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足，需要{cost_money}')
                    return 0
                if Decimal(await data.read("属性", message.author.id, "经验", "0")) < cost_exp:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 经验不足，需要{cost_exp}')
                    return 0
                if value < 1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有剩余的附魔书了')
                    return 0
                book[1][row] = str(value - 1)
                book[1][underline] = str(int(book[1][underline]) + 1)
                yfm.remove(fm)
                print(yfm)
                yfm=str(yfm)
                yfm = yfm.replace("'", "")
                yfm = yfm.replace(" ", "")
                await data.write("物品", message.author.id, "附魔书", str(book))
                await data.write("装备", message.author.id, "鱼竿附魔", yfm)
                await data.write("属性", message.author.id, "经验", str(Decimal(await data.read("属性", message.author.id, "经验", "0")) - cost_exp))
                await data.write("货币", message.author.id, "斯玛特", str(Decimal(await data.read("货币", message.author.id, "斯玛特", "0")) - cost_money))
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 祛魔成功！附魔书已放入背包！')

            elif re.match(r"附魔 ?鱼竿 ?(.*)([0-9]+)", message.content) != None:
                fm = re.match(r"附魔 ?鱼竿 ?(.*)([0-9]+)", message.content).group(1)
                fm2 =fm+re.match(r"附魔 ?鱼竿 ?(.*)([0-9]+)", message.content).group(2)
                book = await data.read("物品", message.author.id, "附魔书", "[['空书'],['0']]")
                book = eval(book)
                if fm2 in book[0]:
                    row = book[0].index(fm2)
                    value = int(book[1][row])
                else:
                    book[0].append(fm2)
                    book[1].append("0")
                    value = 0
                if value < 1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有剩余的附魔书了')
                    return 0
                book[1][row] = str(value - 1)
                yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                levelnew = re.findall(r'\d+', fm2)
                levelnew = int(levelnew[0]) if levelnew else None
                print(fm)
                if fm in yfm:
                    levelold =yfm.find(fm)
                    levelold = int(yfm[levelold + len(fm)])
                    sear = fm+str(levelold)
                    if levelnew is not None and levelold is not None:
                        if levelnew > levelold:
                            yfm = yfm.replace(sear, fm2)
                            print(yfm)
                            await data.write("装备",message.author.id,"鱼竿附魔",yfm)
                            await data.write("物品", message.author.id, "附魔书", str(book))
                            await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{fm2}】附魔成功！已自动升级！')
                        else:
                            print(3)
                            await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{fm2}】附魔失败！此位已有更强或相等魔咒')
                else:
                    fm3 = "," + fm2 + "]"
                    yfm = yfm.replace("]", fm3)
                    yfm = yfm.replace("[,", "[")
                    print(yfm)
                    await data.write("装备",message.author.id,"鱼竿附魔",yfm)
                    await data.write("物品", message.author.id, "附魔书", str(book))
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{fm2}】附魔成功！')
            
            elif re.match(r"合成 ?附魔书 ?(.*)([0-9]+)", message.content) != None:
                fm = re.match(r"合成 ?附魔书 ?(.*)([0-9]+)", message.content).group(1)
                fm3 =int(re.match(r"合成 ?附魔书 ?(.*)([0-9]+)", message.content).group(2))-1
                fm2 =fm+str(fm3)
                book = await data.read("物品", message.author.id, "附魔书", "[['空书'],['0']]")
                book = eval(book)
                if fm2 in book[0]:
                    row = book[0].index(fm2)
                    value = int(book[1][row])
                else:
                    book[0].append(fm2)
                    book[1].append("0")
                    value = 0
                if value < 2:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有剩余的附魔书了')
                    return 0
                if fm3+1 > int(await data.read("附魔", fm, "等级上限", "0")):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 附魔等级已达上限，欲升级请使用破限石')
                    return 0
                book[1][row] = str(value - 2)
                fm3 = fm3+1
                fm2 =fm+str(fm3)
                print(fm3)
                if fm2 in book[0]:
                    row = book[0].index(fm2)
                    value = int(book[1][row])
                else:
                    book[0].append(fm2)
                    book[1].append("0")
                    row = book[0].index(fm2)
                    value = int(book[1][row])
                book[1][row] = str(value + 1)
                print(book[1][row])
                await data.write("物品", message.author.id, "附魔书", str(book))
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 合成成功！')

            elif re.match(r"附魔书破限 ?(.*)([0-9]+)", message.content) != None:
                fm = re.match(r"附魔书破限 ?(.*)([0-9]+)", message.content).group(1)
                fm3 =int(re.match(r"附魔书破限 ?(.*)([0-9]+)", message.content).group(2))-1
                fm2 =fm+str(fm3)
                book = await data.read("物品", message.author.id, "附魔书", "[['空书'],['0']]")
                book = eval(book)
                pxs = int(await data.read("物品", message.author.id, "破限石", "0"))
                if pxs < fm3+1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 破限石不足')
                    return 0
                if fm2 in book[0]:
                    row = book[0].index(fm2)
                    value = int(book[1][row])
                else:
                    book[0].append(fm2)
                    book[1].append("0")
                    value = 0
                if value < 1:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有剩余的附魔书了')
                    return 0
                if fm3-2 > int(await data.read("附魔", fm, "等级上限", "0")):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 当前附魔已达极致')
                    return 0
                if fm3 < int(await data.read("附魔", fm, "等级上限", "0")):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 当前附魔还没有达到满级')
                    return 0
                book[1][row] = str(value - 1)
                fm3 = fm3+1
                fm2 =fm+str(fm3)
                print(fm3)
                if fm2 in book[0]:
                    row = book[0].index(fm2)
                    value = int(book[1][row])
                else:
                    book[0].append(fm2)
                    book[1].append("0")
                    row = book[0].index(fm2)
                    value = int(book[1][row])
                book[1][row] = str(value + 1)
                print(book[1][row])
                pxs=pxs-fm3
                await data.write("物品", message.author.id, "破限石", str(pxs))
                await data.write("物品", message.author.id, "附魔书", str(book))
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 合成成功！')

            elif re.match("附魔 ?[鱼渔]{1}[竿杆]{1}",message.content) != None:
                if Decimal(await data.read("属性",message.author.id,"经验","0")) < Decimal("500"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 经验不足')
                    return 0
                await data.write("属性",message.author.id,"经验",str(Decimal(await data.read("属性",message.author.id,"经验","0"))-Decimal("500")))
                num = random.randint(1,5)
                num2 = random.randint(1,100)
                if num == 1:
                    fm = "海之眷顾"
                if num == 2:
                    fm = "饵钓"
                if num == 3:
                    fm = "海之嫌弃"
                if num == 4:
                    fm = "海洋之息"
                if num2 <= 90:
                    fm2 = fm +"1"
                elif num2 <= 99:
                    fm2 = fm +"2"
                elif num2 == 100:
                    fm2 = fm +"3"
                yfm = await data.read("装备",message.author.id,"鱼竿附魔","[]")
                levelnew = re.findall(r'\d+', fm2)
                levelnew = int(levelnew[0]) if levelnew else None
                print(fm)
                if fm in yfm:
                    levelold =yfm.find(fm)
                    levelold = int(yfm[levelold + len(fm)])
                    sear = fm+str(levelold)
                    if levelnew is not None and levelold is not None:
                        if levelnew > levelold:
                            yfm = yfm.replace(sear, fm2)
                            print(yfm)
                            await data.write("装备",message.author.id,"鱼竿附魔",yfm)
                            await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{fm2}】附魔成功！已自动升级！')
                        else:
                            print(3)
                            await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{fm2}】附魔失败！此位已有更强或相等魔咒')
                else:
                    fm3 = "," + fm2 + "]"
                    yfm = yfm.replace("]", fm3)
                    yfm = yfm.replace("[,", "[")
                    print(yfm)
                    await data.write("装备",message.author.id,"鱼竿附魔",yfm)
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 【{fm2}】附魔成功！')

            
                


            

            #银行

            elif message.content == "签到":
                time = Time.localtime(Time.time())
                if await data.read("其他",message.author.id,"签到","0") == f"{str(time[7])}":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 今天你已经签到过了哟~')
                else:
                    num = await data.read("其他","0","签到人数",f"{str(time[7])}.0")
                    match_result = re.match("([0-9]*)-([0-9]*)", num)
                    if match_result and match_result.group() != f"{str(time[7])}":
                        num = f"{str(time[7])}.0"
                    num_peo = re.search("\.([0-9]+)",num).group()
                    num_peo = int(re.search("([0-9]+)",num_peo).group())
                    银行斯玛特 = Decimal(await data.read("货币",message.author.id,"银行斯玛特","0"))
                    if num_peo < 5:
                        add_银行斯玛特 = (Decimal("0.02")*银行斯玛特).quantize(Decimal("0."))
                    else:
                        add_银行斯玛特 = (Decimal("0.005")*银行斯玛特).quantize(Decimal("0."))
                    GodA = await data.read("其他",message.author.id,"吉尔伽美什EX","0")
                    if GodA == "1":
                        add_银行斯玛特 = (Decimal("0.15")*银行斯玛特).quantize(Decimal("0."))
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 附魔技能[吉尔伽美什EX]发动成功！')
                    add_斯玛特 = Decimal(random.randint(40,70))
                    add_yt = Decimal(random.randint(5,13))
                    心灵鸡汤 = ["比你努力的人一大把，人家天天刷题、背书，你又什么资格偷懒、放松","忘掉所有“不可能”的借口，给自己一个坚持的理由","改变世界不用大刀阔斧，小碎步也可以光芒万丈","赢过一次自己，就有赢第二次的勇气","没有谁天生倔强，只是为了梦想而寸步不让","每天告诉自己一次：我真的很不错","之所以能，是因为相信能","天再高又怎样，踮起脚尖就更接近太远","只有让自己更加强大，才能真正撑起一片天","不是每一次的努力都有回报，但如果你一直努力就一定有回报","很多时候，成功就是多坚持一分钟.在一切成定居之前，请不要停下脚步","学会爱这个世界，但随时准备好与之抗争","没有谁的生活会一直完美，但无论什么时候，都要看向前方，满怀希望就会所向披靡","人生可以向上看、向前看、向左看、向右看，但绝不能向后看、向下看","我可以一落千丈，却偏要一鸣惊人","每一个你讨厌的现在，都有一个不够努力的曾经","有一种落差，是你配不上自己的野心，也辜负了所受的苦难","为别人鼓掌的人也是在给自己的声明加油","因为年轻，所以没有选择，只有试试","你跑得快，耳边才全是风声.你跑得慢，耳边自然都是闲言碎语","这个世界根本不存在“不会”这回事，当你失去所有依靠的时候，你自然就什么都会了","徒手攀岩的过程不是克服困难，而是习惯困难","世界上没有什么真相，你相信什么，什么就是真相","只要在正确的时间弹下正确的音符就行了，乐器会自己演奏","在第一千个选择之外，还有第一千零一个可能，有一扇窗等着我打开，然后有光透进来","成功没有快车道，幸福没有高速路.所有的成功，都来自不倦的努力和奔跑，所有的幸福，都来自平凡的奋斗和坚持","脚踏实地，方可仰望星空","今天应做的事没有做，明天再早也是耽误了","偶尔不开心的时候，是快乐正在加载","努力追上那个曾经被赋予重望的自己吧","错过日落余晖，请记得还有满天星辰","你未必出类拔萃，但一定与众不同","生活有望穿秋水的期待，也会有意想不到的惊喜.今天也要努力呀！不管生活多久才变好，都要先把自己变得更好","让自己变得更好，不是为了悦人，而是为了悦己","就算星星碎掉了，溢出来的光也很好看","阳光下灿烂，风雨中奔跑，做自己的梦，走自己的路","咖啡是苦的，理想是酸的，但录取通知书是甜的，未来可期","不为模糊不清的未来担忧，只为清清楚楚的现在努力","你所做的事情，也许暂时看不到成果，但不要灰心，你不是没有成长，而是在扎根","最困难的时候，往往是黎明前的黑暗","乾坤未定，你我皆是黑马；胜负未分，你我皆有可能","敢于向黑暗宣战的人，心里必须充满光明","当你跌入低谷，那正表示你只能往上，不能往下","只有先改变自己的态度，才能改变人生的高度","好运不会总是降临在你的身上，你的努力是唯一能让你站住脚跟的依靠","成功，往往住在失败的隔壁","有的路，你必须一个人走，这不是孤独，而是选择","不是井里没有水，而是你挖得不够深.不是成功来得慢，而是你努力得不够狠","躲起来的星星也努力发光，你也要加油","成功不是凭梦想和希望，而是凭努力和实践","人生最大的喜悦是每个人都说你做不到，你却做到了","我希望躺在向日葵上，即时沮丧，也能朝着太阳","有些事情不是看到希望才去坚持，而是坚持了才看到希望","青年是人生的骄傲，也是时代未来的希望","事在人为，不去做怎么知道行还是不行","少年的肩应该担起草场莺飞和清风明月","不是每个人都能成为自己想要的样子，但至少每个人都可以努力成为自己想要的样子","没有所谓失败，除非你不再尝试","在最暗的夜才能看见最美的星光，人生亦是如此","要和万物一起复苏，然后一起在夏天里快乐成长","即使天空如此遥远，只要你抬头踮起脚尖，阳光总能靠近你多一点","努力的才叫梦想，不努力的就是空想，你所付出的努力，都是这辈子最清晰的时光","生活一直很公平，你投入的时间越多，它回馈你的就越多","保持一颗好奇心，不断尝试新事物，你总会拥有诗和远方","迎着风雨大步向前，凡是没有打败你的，都会让你更加强大","你的人生永远不会辜负你，那些走过的路全都会让你成为独一无二的自己","接受自己的普通，然后拼尽全力去与众不同","要努力，但是不要着急，凡事都应该有过程","只要你还愿意，世界一定会给你惊喜","得意时淡然，失意时泰然","时间，会带来惊喜.只要我们肯认真地，有希望地，走过每一天","我不是天生的王者，但我的骨子里流动着不让我低头的血","那些有自控力的人都值得我敬佩","你笑时，人们与你一道欢笑；你哭时，人们却付之一笑","所到之处皆风景，不必太执着过去，也不要太渴望未来，反之你只会错过你正在经历的风景","记住一个道理，只有自己变优秀了，其他事情才会跟着好起来","再长的路，一步步也能走完；再短的路，不迈开双脚也无法到达","在通往鲜花和掌声的道路上，必定有荆棘","忘掉所有“不可能”的借口，给自己一个坚持的理由","有志始知蓬莱近，无为总党咫尺远","希望是引导人成功的信仰.如果没了希望，便一事无成","放弃不难，但坚持一定很酷","愿你沉淀又执着，对每件热爱的事物既全力以赴又满载而归，变成一个美好的人","目光远大、目标明确的人往往非常自信，而自信与人生的成败息息相关","很难说什么是办不到的事情，因为昨天的梦想，可以是今天的希望，还可以成为明天的现实"]
                    鸡汤 = 心灵鸡汤[random.randint(0,len(心灵鸡汤)-1)]
                    await data.write("其他",message.author.id,"签到",f"{str(time[7])}")
                    await data.write("其他","0","签到人数",f"{str(time[7])}.{num_peo+1}")
                    await data.write("物品",message.author.id,"寻宝券",str(Decimal(await data.read("物品",message.author.id,"寻宝券","0"))+Decimal("1")))
                    await data.write("物品",message.author.id,"樱桃币",str(Decimal(await data.read("物品",message.author.id,"樱桃币","0"))+add_yt))
                    await data.write("货币",message.author.id,"银行斯玛特",str(银行斯玛特+add_银行斯玛特))
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))+add_斯玛特))
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 签到成功\r获得{add_斯玛特}斯玛特,银行利息{add_银行斯玛特}(已自动续存),1张寻宝券,{add_yt}枚樱桃币\r你是今天第{num_peo+1}个签到的玩家\r──────────────\r{鸡汤}')

            elif message.content == "银行":
                await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}>
您的存款为{await data.read("货币",message.author.id,"银行斯玛特","0")}斯玛特
您的欠款为{await data.read("货币",message.author.id,"贷款","0")}斯玛特
输入"银行存/取款 存取额"进行银行操作
输入“银行贷/还款 额度” 进行贷款操作（使用银行余额）
存入银行的钱在第二天签到可以获得0.5%利息（前五签到得2%）''')

            elif re.match("银行(存|取)款 ?([0-9]+)",message.content) != None:
                string = re.search("存|取",message.content).group()
                num = re.search("[0-9]+",message.content).group()
                if string == "存":
                    if Decimal(await data.read("货币",message.author.id,"斯玛特","0")) < Decimal(num):
                        await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 余额不足''')
                    else:
                        await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(num)))
                        await data.write("货币",message.author.id,"银行斯玛特",str(Decimal(await data.read("货币",message.author.id,"银行斯玛特","0"))+Decimal(num)))
                        await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 存款成功''')
                else:
                    if Decimal(await data.read("货币",message.author.id,"银行斯玛特","0")) < Decimal(num):
                        await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 存款不足''')
                    else:
                        await data.write("货币",message.author.id,"银行斯玛特",str(Decimal(await data.read("货币",message.author.id,"银行斯玛特","0"))-Decimal(num)))
                        await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))+Decimal(num)))
                        await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 取款成功''')
                
            elif re.match("银行贷款 ?([0-9]+)",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                num = Decimal(num)
                allm = Decimal(await data.read("货币",message.author.id,"贷款","0"))
                allm = num+allm
                if allm >2000000:
                    await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 只允许200w内贷款''')
                    return 0
                await data.write("货币",message.author.id,"贷款",str(allm))
                await data.write("货币",message.author.id,"银行斯玛特",str(Decimal(await data.read("货币",message.author.id,"银行斯玛特","0"))+Decimal(num)))
                await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 贷款成功，已存入银行''')

            elif re.match("银行还款 ?([0-9]+)",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                num = Decimal(num)
                allm = Decimal(await data.read("货币",message.author.id,"贷款","0"))
                allm = allm-num
                if allm <0:
                    await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 你还的太多了''')
                    return 0
                await data.write("货币",message.author.id,"贷款",str(allm))
                await data.write("货币",message.author.id,"银行斯玛特",str(Decimal(await data.read("货币",message.author.id,"银行斯玛特","0"))-Decimal(num)))
                await self.api.post_message(channel_id=message.channel_id, content=f'''<@!{message.author.id}> 还款成功，已扣除银行余额''')

            elif re.match("转账<@![0-9]+> ?([0-9]+)", message.content) != None:
                pattern = r"转账<@!([0-9]+)> ?([0-9]+)"
                user_id = str(message.mentions[0].id)
                amount = Decimal(re.match(pattern, message.content).group(2))
                time = Time.localtime(Time.time())
                if await data.read("其他",user_id,"签到","0") == f"{str(time[7])}":
                    sender_balance = Decimal(await data.read("货币", message.author.id, "斯玛特", 0))
                    if sender_balance >= amount:
                        await data.write("货币", message.author.id, "斯玛特", str(sender_balance - amount))
                        recipient_balance = Decimal(await data.read("货币", user_id, "斯玛特", 0))
                        await data.write("货币", user_id, "斯玛特", str(recipient_balance + amount))
                        await self.api.post_message(channel_id=message.channel_id, content=f'转账成功！\r你的斯玛特：{sender_balance-amount}\r对方斯玛特：{recipient_balance+amount}')
                    else:
                        await self.api.post_message(channel_id=message.channel_id, content=f'你的斯玛特不够，无法转账')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'对方未签到')

            #村庄

            elif message.content == "村庄":
                if await data.read("村庄_村民",message.author.id,"归属村庄","0") == "0":
                    num = "1"
                    if num == "0":
                        return 0
                    if int(num) > 10:
                        return 0
                    总人数1 = "0"
                    创建者1 = await data.read("村庄",str((int(num)-1)*3+1),"村庄创建者","0")
                    if 创建者1 != "0":
                        player1 = eval(await data.read("村庄",str((int(num)-1)*3+1),"村庄玩家","[]"))
                        npc1 = eval(await data.read("村庄",str((int(num)-1)*3+1),"村庄npc","[]")) 
                        总人数1 = len(player1) + len(npc1)
                    总人数2 = "0"
                    创建者2 = await data.read("村庄",str((int(num)-1)*3+2),"村庄创建者","0")
                    if 创建者2 != "0":
                        player2 = eval(await data.read("村庄",str((int(num)-1)*3+2),"村庄玩家","[]"))
                        npc2 = eval(await data.read("村庄",str((int(num)-1)*3+2),"村庄npc","[]")) 
                        总人数2 = len(player2) + len(npc2)
                    总人数3 = "0"
                    创建者3 = await data.read("村庄",str(int(num)*3),"村庄创建者","0")
                    if 创建者3 != "0":
                        player3 = eval(await data.read("村庄",str(int(num)*3),"村庄玩家","[]"))
                        npc3 = eval(await data.read("村庄",str(int(num)*3),"村庄npc","[]")) 
                        总人数3 = len(player3) + len(npc3)
                    await self.api.post_message(channel_id=message.channel_id, content=f'''村庄列表
No.{str((int(num)-1)*3+1)}【{await data.read("村庄",str((int(num)-1)*3+1),"村庄名","0")}】
创建者：{创建者1}
总人数：{总人数1}
村庄等级：{await data.read("村庄",str((int(num)-1)*3+1),"村庄等级","0")}

No.{str((int(num)-1)*3+2)}【{await data.read("村庄",str((int(num)-1)*3+2),"村庄名","0")}】
创建者：{创建者2}
总人数：{总人数2}
村庄等级：{await data.read("村庄",str((int(num)-1)*3+2),"村庄等级","0")}

No.{str(int(num)*3)}【{await data.read("村庄",str(int(num)*3),"村庄名","0")}】
创建者：{创建者3}
总人数：{总人数3}
村庄等级：{await data.read("村庄",str(int(num)*3),"村庄等级","0")}
————
请输入：村庄第{min(int(num)+1,10)}页 加入村庄+序号  创建村庄指南
''')
                else:
                    village =await data.read("村庄_村民",message.author.id,"归属村庄","0")
                    player = eval(await data.read("村庄","1","村庄玩家","[]"))
                    npc = eval(await data.read("村庄","1","村庄npc","[]")) 
                    await self.api.post_message(channel_id=message.channel_id, content=f'''【{await data.read("村庄",village,"村庄名","0")}】
Level.{await data.read("村庄",village,"村庄等级","0")}
创建者：{await data.read("村庄",village,"村庄创建者","0")}
总人数：{len(player)+len(npc)}
 · NPC数：{len(npc)}
 · 玩家数：{len(player)}
村庄贡献：{await data.read("村庄_村民",message.author.id,"村庄贡献","0")}
钓鱼次数：{await data.read("村庄",village,"钓鱼次数",'0')}
村庄财富：{await data.read("村庄",village,"村庄财富","0")}
村庄仓库 | 村庄建筑
村庄商店 | 管理村庄''')

            elif re.match("村庄 ?第 ?([0-9]+) ?页",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                if num == "0":
                    return 0
                if int(num) > 10:
                    return 0
                总人数1 = "0"
                创建者1 = await data.read("村庄",str((int(num)-1)*3+1),"村庄创建者","0")
                if 创建者1 != "0":
                    player1 = eval(await data.read("村庄",str((int(num)-1)*3+1),"村庄玩家","[]"))
                    npc1 = eval(await data.read("村庄",str((int(num)-1)*3+1),"村庄npc","[]")) 
                    总人数1 = len(player1) + len(npc1)
                总人数2 = "0"
                创建者2 = await data.read("村庄",str((int(num)-1)*3+2),"村庄创建者","0")
                if 创建者2 != "0":
                    player2 = eval(await data.read("村庄",str((int(num)-1)*3+2),"村庄玩家","[]"))
                    npc2 = eval(await data.read("村庄",str((int(num)-1)*3+2),"村庄npc","[]")) 
                    总人数2 = len(player2) + len(npc2)
                总人数3 = "0"
                创建者3 = await data.read("村庄",str(int(num)*3),"村庄创建者","0")
                if 创建者3 != "0":
                    player3 = eval(await data.read("村庄",str(int(num)*3),"村庄玩家","[]"))
                    npc3 = eval(await data.read("村庄",str(int(num)*3),"村庄npc","[]")) 
                    总人数3 = len(player3) + len(npc3)
                await self.api.post_message(channel_id=message.channel_id, content=f'''村庄列表
No.{str((int(num)-1)*3+1)}【{await data.read("村庄",str((int(num)-1)*3+1),"村庄名","0")}】
创建者：{创建者1}
总人数：{总人数1}
村庄等级：{await data.read("村庄",str((int(num)-1)*3+1),"村庄等级","0")}

No.{str((int(num)-1)*3+2)}【{await data.read("村庄",str((int(num)-1)*3+2),"村庄名","0")}】
创建者：{创建者2}
总人数：{总人数2}
村庄等级：{await data.read("村庄",str((int(num)-1)*3+2),"村庄等级","0")}

No.{str(int(num)*3)}【{await data.read("村庄",str(int(num)*3),"村庄名","0")}】
创建者：{创建者3}
总人数：{总人数3}
村庄等级：{await data.read("村庄",str(int(num)*3),"村庄等级","0")}
————
请输入：村庄第{min(int(num)+1,10)}页 加入村庄+序号  创建村庄指南
''')
                
            elif re.match("(创建村庄指南|管理村庄){1}",message.content) != None:
                await self.api.post_message(channel_id=message.channel_id, content='''·如果你想要创建村庄，需要至少Level.5及200w斯玛特
·指令：创建村庄 村庄名\r
·管理指令：
 · 招募村民
 · 查看申请
 · 建造村庄建筑+建筑
 · 设置权限等级+num+@.*
''')
            elif re.match("设置权限等级([0-9]+)<@![0-9]+>",message.content) != None:
                iidd = str(message.mentions[0].id)
                num = re.search("[0-9]+", message.content).group()
                if await data.read("村庄_村民",message.author.id,"归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没加入任何村庄呢")
                    return 0
                if int(await data.read("村庄_村民",message.author.id,"权力等级","0")) <= 9:
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 权限不足")
                    return 0
                if await data.read("村庄_村民",iidd,"归属村庄","0") != await data.read("村庄_村民",message.author.id,"归属村庄","0"):
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你和他不是一个村的")
                    return 0
                if Decimal(num) > 9:
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 最高9级，10级为村长")
                    return 0
                await data.write("村庄_村民",iidd,"权力等级",str(num))
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 权限设置成功")
            elif re.match(r"创建村庄 ?(.*)",message.content) != None:
                village = re.match(r"创建村庄 ?(.*)",message.content).group(1)
                if Decimal(await data.read("属性",message.author.id,"等级","0")) < Decimal("5"):
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你需要Level.5才能创建村庄")
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0")) < Decimal("2000000"):
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你需要200w斯玛特才能创建村庄")
                    return 0
                if await data.read("村庄_村民",message.author.id,"归属村庄","0") != "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你已经加入一个村庄了")
                    return 0
                num = int(await data.read("村庄",'0',"村庄数量","0"))
                num += 1
                list_villager = eval(await data.read("村庄",str(num),"村庄申请","[[],[]]"))
                await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal("2000000")))
                await data.write("村庄",'0',"村庄数量",str(num))
                num = str(num)
                await data.write("村庄",num,"村庄名",f"{village}")
                await data.write("村庄",num,"村庄创建者",f"{message.author.username}({message.author.id})")
                await data.write("村庄",num,"村庄等级",'0')
                await data.write("村庄",num,"钓鱼次数",'0')
                await data.write("村庄",num,"村庄玩家",f"""["{message.author.username}({message.author.id})"]""")
                await data.write("村庄",num,"村庄职位","""{"0":"0级权限","1":"1级权限","2":"2级权限","3":"3级权限","4":"4级权限","5":"5级权限","6":"6级权限","7":"7级权限","8":"8级权限","9":"9级权限","10":"最高级权限"}""")
                await data.write("村庄_村民",message.author.id,"归属村庄",num)
                await data.write("村庄_村民",message.author.id,"权力等级","10")
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 创建成功!\r你的编号: No.{num}")

            elif re.match(r"加入村庄 ?([0-9]+)",message.content) != None:
                village = re.search(r"([0-9]+)",message.content).group()
                if village == "0" or int(village) > 30:
                    return 0
                if Decimal(await data.read("属性",message.author.id,"等级","0")) < Decimal("3"):
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你需要Level.3才能加入村庄")
                    return 0
                if await data.read("村庄_村民",message.author.id,"归属村庄","0") != "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你已经加入一个村庄了")
                    return 0
                list_villager = eval(await data.read("村庄",village,"村庄申请","[[],[]]"))
                list_villager[0].append(message.author.id)
                list_villager[1].append(message.author.username)
                print(list_villager)
                await data.write("村庄",village,"村庄申请",f"{list_villager}")
                await data.read("村庄_村民",message.author.id,"加入村庄缓存",village)
                await self.api.post_message(channel_id=message.channel_id, content="申请成功!\r请等待村管理成员审核!")

            elif message.content == "查看申请":
                if await data.read("村庄_村民",message.author.id,"归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没加入任何村庄呢")
                    return 0
                if int(await data.read("村庄_村民",message.author.id,"权力等级","0")) <= 0:
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 权限不足")
                    return 0
                msg = f'【{await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄名","0")}】'
                list_villager = eval(await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄申请","[[],[]]"))
                if list_villager == [[],[]]:
                    msg += "0"
                else:
                    i = 0
                    while i < len(list_villager[0]):
                        msg += "\r" + list_villager[1][i] + "(" + list_villager[0][i] + ")"
                        i += 1
                await self.api.post_message(channel_id=message.channel_id, content=msg)

            elif re.match(r"同意申请 ?<@![0-9]+>",message.content) != None:
                villager = str(message.mentions[0].id)
                if await data.read("村庄_村民",message.author.id,"归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没加入任何村庄呢")
                    return 0
                if int(await data.read("村庄_村民",message.author.id,"权力等级","0")) <= 0:
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 权限不足")
                    return 0
                list_villager = eval(await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄申请","[[],[]]"))
                num = await data.read("村庄_村民",message.author.id,"归属村庄","0")
                if villager in list_villager[0]:
                    n = list_villager[0].index(villager)
                    await data.write("村庄_村民",villager,"归属村庄",num)
                    await self.api.post_message(channel_id=message.channel_id, content=f"""<@!{message.author.id}> 操作成功!恭喜{list_villager[1][n]}加入【{await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄名","0")}】!""")
                    player = eval(await data.read("村庄",num,"村庄玩家","0"))
                    player.append(f"{list_villager[0][n]}({list_villager[1][n]})")
                    await data.write("村庄",num,"村庄玩家",f"""{player}""")
                    await data.write("村庄_村民",villager,"权力等级","0")
                    list_villager[0].pop(n)
                    list_villager[1].pop(n)
                    await data.write("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"申请列表",f"{list_villager}")
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 对方没有申请加入你的村庄")

            elif re.match(r"拒绝申请 ?<@![0-9]+>",message.content) != None:
                villager = int(message.mentions[0].id)
                if await data.read("村庄_村民",message.author.id,"归属村庄","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没加入任何村庄呢")
                    return 0
                if int(await data.read("村庄_村民",message.author.id,"权力等级","0")) <= 0:
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 权限不足")
                    return 0
                list_villager = eval(await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄申请","[[],[]]"))
                if villager in list_villager[0]:
                    n = list_villager[0].index(villager)
                    await self.api.post_message(channel_id=message.channel_id, content=f"""<@!{message.author.id}> 操作成功!{list_villager[1][n]}没能加入【{await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄名","0")}】!""")
                    list_villager[0].pop(n)
                    list_villager[1].pop(n)
                    await data.write("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"申请列表",f"{list_villager}")
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 对方没有申请加入你的村庄")
            
            elif re.match("玩家 ?第 ?([0-9]+) ?页",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                if num == "0":
                    return 0
                msg = f'''【{await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄名","0")}】玩家第{num}页'''
                i = (int(num)-1)*10
                list_villager = eval(await data.read("村庄",await data.read("村庄_村民",message.author.id,"归属村庄","0"),"村庄玩家","0"))
                while i < int(num)*10 and i < len(list_villager):
                    msg += "\rNo." + str(i+1) + list_villager[i]
                    i += 1
                await self.api.post_message(channel_id=message.channel_id, content=msg)

            elif message.content == "村庄仓库":
                village = await data.read("村庄_村民",message.author.id,"归属村庄","0")
                if village == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你还没有村庄")
                    return 0
                village_name = await data.read("村庄",village,"村庄名","0")
                斯玛特 = await data.read("村庄_仓库",village,"斯玛特","0")
                农场币 = await data.read("村庄_仓库",village,"农场币","0")
                兑换券 = await data.read("村庄_仓库",village,"兑换券","0")
                鱼竿 = await data.read("村庄_仓库",village,"鱼竿","0")
                小刀 = await data.read("村庄_仓库",village,"小刀","0")
                头盔 = await data.read("村庄_仓库",village,"头盔","0")
                钱袋 = await data.read("村庄_仓库",village,"钱袋","0")
                渔网 = await data.read("村庄_仓库",village,"渔网","0")
                附魔书 = await data.read("村庄_仓库",village,"附魔书","[[],[]]")
                装备 = await data.read("村庄_仓库",village,"装备","0")
                破限石 = await data.read("村庄_仓库",village,"破限石","0")
                鱼 = await data.read("村庄_仓库",village,"鱼","0")
                await self.api.post_message(channel_id=message.channel_id, content=f'村庄 {village_name} 的仓库\n斯玛特：{斯玛特}\n农场币：{农场币}\n兑换券：{兑换券}\n鱼竿：{鱼竿}\n渔网：{渔网}\n小刀：{小刀}\n头盔：{头盔}\n钱袋：{钱袋}\n破限石：{破限石}\n鱼：{鱼}\n附魔书：{附魔书}\n装备：{装备}\n村庄仓库使用：\n分配(物品名)(数量)@指定人\n设置村庄仓库分配权限 (开/关) @指定人\n村庄仓库贡献(物品名)(数量)')

            elif re.match("设置?(村庄)?仓库分配(权限)? ?(开|关){1} ?<@![0-9]+>",message.content) != None:
                if await data.read("村庄_村民",message.author.id,"权力等级","0") != "10":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 权限不足")
                    return 0
                mode = re.match("设置?(村庄)?仓库分配(权限)? ?(开|关){1} ?<@![0-9]+>",message.content).group(3)
                user_id = message.mentions[0].id
                if mode == "开":
                    mode = "1"
                else:
                    mode = "0"
                await data.write("村庄_村民",user_id,"仓库权限",mode)
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 设置成功, 已{mode}")

            elif re.match(r"分配 ?([^0-9\s]+[0-9]?) ?([0-9]+) ?<@![0-9]+>",message.content) != None:
                print("匹配成功")
                user_id = message.mentions[0].id
                village = await data.read("村庄_村民",message.author.id,"归属村庄","0")
                if village == "0":
                    await self.api.post_message(channel_id=message.channel_id, contesnt=f"<@!{message.author.id}> 你还没有村庄")
                    return 0
                if await data.read("村庄_村民",message.author.id,"仓库权限","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 权限不足")
                    return 0
                fm = re.match(r"分配 ?([^0-9\s]+[0-9]?) ?([0-9]+) ?<@![0-9]+>", message.content).group(1)
                fm2 = Decimal(re.match(r"分配 ?([^0-9\s]+[0-9]?) ?([0-9]+) ?<@![0-9]+>", message.content).group(2))
                fms = eval(await data.read("物品",user_id,"附魔书","[[],[]]"))
                cfms = eval(await data.read("村庄_仓库",village,"附魔书","[[],[]]"))
                if fm == "斯玛特":
                    item = Decimal(await data.read("村庄_仓库",village,"斯玛特","0"))
                    if item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你村没钱")
                        return 0
                    item = item - fm2
                    await data.write("村庄_仓库",village,"斯玛特",str(item))
                    money = await data.read("货币",user_id,"斯玛特","0")
                    money = str(Decimal(money)+fm2)
                    await data.write("货币",user_id,"斯玛特",money)
                elif fm == "农场币":
                    item = Decimal(await data.read("村庄_仓库",village,"农场币","0"))
                    if item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你村没钱")
                        return 0
                    item = item - fm2
                    await data.write("村庄_仓库",village,"农场币",str(item))
                    money = await data.read("货币",user_id,"农场币","0")
                    money = str(Decimal(money)+fm2)
                    await data.write("货币",user_id,"农场币",money)
                elif fm == "鱼":
                    item = Decimal(await data.read("村庄_仓库",village,"鱼","0"))
                    if item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你村没鱼")
                        return 0
                    item = item - fm2
                    await data.write("村庄_仓库",village,"鱼",str(item))
                    money = await data.read("数据",user_id,"鱼","0")
                    money = str(Decimal(money)+fm2)
                    await data.write("数据",user_id,"鱼",money)
                elif fm == "兑换券" or fm == "破限石":
                    item = Decimal(await data.read("村庄_仓库",village,fm,"0"))
                    if item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你村没券")
                        return 0
                    item = item - fm2
                    await data.write("村庄_仓库",village,fm,str(item))
                    money = await data.read("物品",user_id,fm,"0")
                    money = str(Decimal(money)+fm2)
                    await data.write("物品",user_id,fm,money)
                elif fm == "鱼竿" or fm == "小刀" or fm == "头盔" or fm == "钱袋" or fm == "渔网":
                    item = Decimal(await data.read("村庄_仓库",village,fm,"0"))
                    if item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你村没{fm}")
                        return 0
                    item = item - fm2
                    await data.write("村庄_仓库",village,fm,str(item))
                    money = await data.read("装备",user_id,fm,"0")
                    money = str(Decimal(money)+fm2)
                    await data.write("装备",user_id,fm,money)
                elif fm in cfms[0]:
                    cfmi = cfms[0].index(fm)
                    try:
                        fmi = fms[0].index(fm)
                    except:
                        fms[0].append(fm)
                        fms[1].append("0")
                        fmi = fms[0].index(fm)
                    fmn = Decimal(fms[1][fmi])
                    cfmn = Decimal(cfms[1][cfmi])
                    if cfmn < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你村没书")
                        return 0
                    fms[1][fmi] = str(fmn+fm2)
                    cfms[1][cfmi] = str(cfmn-fm2)
                    await data.write("物品",user_id,"附魔书",str(fms))
                    await data.write("村庄_仓库",village,"附魔书",str(cfms))
                else:
                    print(fm)
                    print(fm2)
                    print(fms)
                    print(cfms)
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 类型错误(或无此附魔书)")
                    return 0
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 分配成功")

            elif re.match(r"村庄仓库贡献 ?([^0-9\s]+[0-9]?) ?([0-9]+)",message.content) != None:
                village = await data.read("村庄_村民",message.author.id,"归属村庄","0")
                user_id=message.author.id
                if village == "0":
                    await self.api.post_message(channel_id=message.channel_id, contesnt=f"<@!{message.author.id}> 你还没有村庄")
                    return 0
                fm = re.match(r"村庄仓库贡献 ?([^0-9\s]+[0-9]?) ?([0-9]+)", message.content).group(1)
                fm2 = Decimal(re.match(r"村庄仓库贡献 ?([^0-9\s]+[0-9]?) ?([0-9]+)", message.content).group(2))
                fms = eval(await data.read("物品",message.author.id,"附魔书","[[],[]]"))
                cfms = eval(await data.read("村庄_仓库",village,"附魔书","[[],[]]"))
                if fm == "斯玛特" or fm == "农场币":
                    item = Decimal(await data.read("村庄_仓库",village,fm,"0"))
                    p_item = Decimal(await data.read("货币",message.author.id,fm,"0"))
                    if p_item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没钱")
                        return 0
                    item = item + fm2
                    await data.write("村庄_仓库",village,fm,str(item))
                    p_item = str(p_item-fm2)
                    await data.write("货币",message.author.id,fm,p_item)
                elif fm == "鱼":
                    item = Decimal(await data.read("村庄_仓库",village,fm,"0"))
                    p_item = Decimal(await data.read("数据",message.author.id,fm,"0"))
                    if p_item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没鱼")
                        return 0
                    item = item + fm2
                    await data.write("村庄_仓库",village,fm,str(item))
                    p_item = str(p_item-fm2)
                    await data.write("数据",message.author.id,fm,p_item)
                elif fm == "兑换券" or fm == "破限石":
                    item = Decimal(await data.read("村庄_仓库",village,fm,"0"))
                    p_item = Decimal(await data.read("物品",message.author.id,fm,"0"))
                    if p_item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没券")
                        return 0
                    item = item + fm2
                    await data.write("村庄_仓库",village,fm,str(item))
                    p_item = str(p_item-fm2)
                    await data.write("物品",user_id,fm,p_item)
                elif fm == "鱼竿" or fm == "小刀" or fm == "头盔" or fm == "钱袋" or fm == "渔网":
                    item = Decimal(await data.read("村庄_仓库",village,fm,"0"))
                    p_item = Decimal(await data.read("装备",message.author.id,fm,"0"))
                    if p_item <49:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 等级过低，需要49级")
                        return 0
                    if p_item < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没{fm}")
                        return 0
                    item = item + fm2
                    await data.write("村庄_仓库",village,fm,str(item))
                    p_item = str(p_item-fm2)
                    await data.write("装备",user_id,fm,p_item)
                elif fm in fms[0]:
                    fmi = fms[0].index(fm)
                    try:
                        cfmi = cfms[0].index(fm)
                    except:
                        cfms[0].append(fm)
                        cfms[1].append("0")
                        cfmi = cfms[0].index(fm)
                    fmn = Decimal(fms[1][fmi])
                    cfmn = Decimal(cfms[1][cfmi])
                    if fmn < fm2:
                        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你没书")
                        return 0
                    fms[1][fmi] = str(fmn-fm2)
                    cfms[1][cfmi] = str(cfmn+fm2)
                    print(cfmn)
                    print(fm2)
                    print(cfmn+fm2)
                    await data.write("物品",message.author.id,"附魔书",str(fms))
                    await data.write("村庄_仓库",village,"附魔书",str(cfms))
                else:
                    print(fm)
                    print(fm2)
                    print(fms)
                    print(cfms)
                    await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 类型错误(或无此附魔书)")
                    return 0
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 贡献成功")
                


            #商店

            elif message.content == '商店':
                await self.api.post_message(channel_id=message.channel_id, content='''┌─商店─┐
├杂物商店┤
├钓鱼商店┤
├装备商店┤
├附魔商店┤
├农具商店┤
├婚戒商店┤
├兑换商店┤
├头衔商店┤
├房产市场┤
├家具市场┤
└────┘''')

            #杂物商店

            elif message.content == '杂物商店':
                await self.api.post_message(channel_id=message.channel_id, content='''杂物商店
面包：5斯玛特
*恢复8体力
健力宝：10斯玛特
*恢复1精力
[装备]咖啡帽：100斯玛特
*每小时可领取免费的11体力和3精力(输入:喝咖啡)
输入"买+物品名称+份数"购买''')
                
            elif message.content == '附魔商店':
                await self.api.post_message(channel_id=message.channel_id, content='''附魔商店
空附魔书：200w斯玛特
*可以用于祛魔并成为附魔书
海之后裔附魔书：3000鱼
*有几率钓鱼成果翻倍
输入"买+物品名称+份数"购买''')
            elif re.match("买 ?空附魔书 ?([0-9]+)",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(num)*2000000:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                    return 0
                await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(num)*Decimal("2000000")))
                book = await data.read("物品", message.author.id, "附魔书", "[['空书'],['0']]")
                book = eval(book)
                if "空书" in book[0]:
                    row = book[0].index("空书")
                    value = int(book[1][row])
                else:
                    book[0].append("空书")
                    book[1].append("0")
                    row = book[0].index("空书")
                    value = 0
                num = int(num)
                book[1][row] = str(value + num)
                await data.write("物品", message.author.id, "附魔书", str(book))  
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
            elif re.match("买 ?海之后裔附魔书 ?([0-9]+)",message.content) != None:
                if await data.read("其他",message.author.id,"量子之海","0")=="1" or await data.read("其他",message.author.id,"海的女儿","0")=="1":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有更强力附魔了')
                    return 0
                num = re.search("[0-9]+",message.content).group()
                if Decimal(await data.read("数据",message.author.id,"鱼","0"))<Decimal(num)*3000:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 鱼不足')
                    return 0
                await data.write("数据",message.author.id,"鱼",str(Decimal(await data.read("数据",message.author.id,"鱼","0"))-Decimal(num)*Decimal("3000")))
                book = await data.read("物品", message.author.id, "附魔书", "[['空书'],['0']]")
                book = eval(book)
                if "海之后裔1" in book[0]:
                    row = book[0].index("海之后裔1")
                    value = int(book[1][row])
                else:
                    book[0].append("海之后裔1")
                    book[1].append("0")
                    row = book[0].index("海之后裔1")
                    value = 0
                num = int(num)
                book[1][row] = str(value + num)
                await data.write("物品", message.author.id, "附魔书", str(book))  
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
            elif re.match("买 ?面包 ?([0-9]+)",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(num)*5:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    msg = await data.属性操作(message.author.id,"体力",Decimal("8")*Decimal(num),"add")
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功\r{msg}')
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(num)*Decimal("5")))

            elif re.match("买 ?健力宝 ?([0-9]+)",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(num)*5:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    msg = await data.属性操作(message.author.id,"精力",Decimal(num),"add")
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功\r{msg}')
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(num)*Decimal("10")))

            elif re.match("买 ?咖啡帽",message.content) != None:
                if await data.read("装备",message.author.id,"咖啡帽","0") == "1":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有咖啡帽了')
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal("100"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("装备",message.author.id,"咖啡帽","1")
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal("100")))

            elif message.content == "喝咖啡":
                if await data.read("装备",message.author.id,"咖啡帽","0") == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有咖啡帽')
                else:
                    time = Time.localtime(Time.time())
                    if await data.read("其他",message.author.id,"喝咖啡","0") == f"{str(time[2])}-{str(time[3])}":
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 这小时你已经喝过咖啡了')
                    else:
                        msg1 = await data.属性操作(message.author.id,"精力","3","add")
                        msg2 = await data.属性操作(message.author.id,"体力","11","add")
                        await data.write("其他",message.author.id,"喝咖啡",f"'{str(time[2])}-{str(time[3])}'")
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 喝咖啡成功\r{msg1}\t{msg2}')

            #钓鱼商店

            elif message.content == '钓鱼商店':
                await self.api.post_message(channel_id=message.channel_id, content='''钓鱼商店
鱼饵—2斯玛特—钓鱼必需消耗品
1级鱼竿—40斯玛特—钓鱼用具—获取5~9斯玛特
2级鱼竿—100斯玛特—钓鱼用具—获取6~11斯玛特
3级鱼竿—230斯玛特—钓鱼用具—获取7~13斯玛特
4级鱼竿—520斯玛特—钓鱼用具—获取8~15斯玛特
5级鱼竿—999斯玛特—钓鱼用具—获取9~17斯玛特
6级鱼竿—1666斯玛特—钓鱼用具—获取10~19斯玛特
9级鱼竿—7777斯玛特—20%多上钩1鱼—获取13~25斯玛特
9级鱼竿+—强化获取—(20+2*强化等级)%—(获取13+0.5*强化等级)~(25+强化等级)斯玛特
韧线1—100斯玛特—25%鱼逃跑失败
韧线2—233斯玛特—50%鱼逃跑失败
韧线3—500斯玛特—75%鱼逃跑失败
韧线4—500w斯玛特—100%鱼逃跑失败
渔网—50w斯玛特—10%多上钩1鱼
输入买+物品购买(鱼饵需要+数量)''')

            elif re.match("买 ?鱼饵 ?([0-9]+)",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(num)*2:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("物品",message.author.id,"鱼饵",str(Decimal(await data.read("物品",message.author.id,"鱼饵","0"))+Decimal(num)))
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(num)*2))

            elif re.match("买 ?(1|2|3|4|5|6|9){1} ?级 ?鱼(竿|杆){1}",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                鱼竿价格 = {"1":"40","2":"100","3":"230","4":"520","5":"999","6":"1666","9":"7777"}
                if Decimal(await data.read("装备",message.author.id,"鱼竿","0")) >= Decimal(num):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有更高级的鱼竿了')
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(鱼竿价格[num]):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("装备",message.author.id,"鱼竿",num)
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(鱼竿价格[num])))

            elif re.match("强化 ?(渔|鱼){1}(竿|杆){1} ?准备",message.content) != None:
                trj = Decimal(await data.read("其他",message.author.id,"鱼竿投入","0"))
                if trj < Decimal("500"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 基础金不足')
                    return 0
                qh_state[message.author.id] = 1
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 准备完毕，再次输入强化鱼竿来强化')

            elif re.match("强化 ?(渔|鱼){1}(竿|杆){1} ?([0-9]*)",message.content) != None:
                yug = Decimal(await data.read("装备",message.author.id,"鱼竿","0"))
                if yug < Decimal("9"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你还没有9级鱼竿呢')
                    return 0
                trj = Decimal(await data.read("其他",message.author.id,"鱼竿投入","0"))
                成功率 = min(Decimal('100'),max(Decimal("0"),(Decimal("105")-yug*Decimal("5")+max(Decimal("0"),trj-Decimal("500"))/Decimal(3)/(yug-Decimal(8))).quantize(Decimal('0.0000'))))
                if re.search("[0-9]+",message.content) != None:
                    斯玛特 = Decimal(await data.read("货币",message.author.id,"斯玛特","0"))
                    if 斯玛特 < Decimal(re.search("[0-9]+",message.content).group()):
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                        return 0
                    await data.write("货币",message.author.id,"斯玛特",str(斯玛特-Decimal(re.search("[0-9]+",message.content).group())))
                    await data.write("其他",message.author.id,"鱼竿投入",str(Decimal(await data.read("其他",message.author.id,"鱼竿投入","0"))+Decimal(re.search("[0-9]+",message.content).group())))
                    trj = Decimal(await data.read("其他",message.author.id,"鱼竿投入","0"))
                    成功率 = min(Decimal('100'),max(Decimal("0"),(Decimal("105")-yug*Decimal("5")+max(Decimal("0"),trj-Decimal("500"))/Decimal(3)/(yug-Decimal(8))).quantize(Decimal('0.0000'))))
                try:
                    qh_state[message.author.id] = qh_state[message.author.id]
                except:
                    qh_state[message.author.id] = 0
                if qh_state[message.author.id] == 1:
                    qh_state[message.author.id] = 0
                    await data.write("其他",message.author.id,"鱼竿投入","0")
                    if random.uniform(0,99) < 成功率:
                        await data.write("装备",message.author.id,"鱼竿",str(yug+Decimal("1")))
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 强化成功\r9级鱼竿+{yug-Decimal("9")}已强化至9级鱼竿+{yug-Decimal("8")}')
                        await data.write("其他",message.author.id,"鱼竿保级","0")
                    else:
                        if yug == Decimal("9") or await data.read("其他",message.author.id,"鱼竿保级","0") == "1":
                            await data.write("其他",message.author.id,"鱼竿保级","0")
                            await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 强化失败，本次不掉级')
                        else:
                            await data.write("装备",message.author.id,"鱼竿",str(yug-Decimal("1")))
                            await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 强化失败\r9级鱼竿+{yug-Decimal("9")}已掉级成9级鱼竿+{yug-Decimal("10")}')
                else:
                    if await data.read("其他",message.author.id,"鱼竿保级","0") == "0":
                        保 = "否"
                    else:
                        保 = "是"
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}>\r强化至9级鱼竿+{yug-Decimal("8")}准备\r基础需要:({min(Decimal("500"),trj)}/500)\r额外投入:{max(trj-Decimal(500),Decimal("0"))}\r成功率:{成功率}%\r保级:{保}\r输入“强化鱼竿+金额”投入斯玛特\r输入“买鱼竿保级卡”保级,{yug*(yug-Decimal("8"))*Decimal("20")+Decimal("300")}斯玛特\r输入“强化鱼竿准备”准备强化')

            elif re.match("买 ?(1|2|3|4){1} ?级 ?韧线",message.content) != None or re.match("买 ?韧线 ?(1|2|3|4){1}",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                韧线价格 = {"1":"100","2":"233","3":"500","4":"5000000"}
                if Decimal(await data.read("装备",message.author.id,"韧线","0")) >= Decimal(num):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有更高级的韧线了')
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(韧线价格[num]):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("装备",message.author.id,"韧线",num)
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(韧线价格[num])))
 
            elif re.match("买 ?(渔|鱼){1}网",message.content) != None:
                if await data.read("装备",message.author.id,"渔网","0") == "1":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有渔网了')
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal("500000"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("装备",message.author.id,"渔网","1")
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal("500000")))

            elif re.match("强化 ?(渔|鱼){1}网 ?([0-9]*)",message.content) != None:
                yuw = await data.read("装备",message.author.id,"渔网","0")
                if yuw == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你还没有渔网呢')
                    return 0
                if yuw == "10":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的渔网已经满级啦！')
                    return 0
                强化需求 = {"1":"500000","2":"1000000","3":"2000000","4":"3000000","5":"4000000","6":"5000000","7":"6000000","8":"7000000","9":"10000000"}
                if re.search("[0-9]+",message.content) != None:
                    斯玛特 = Decimal(await data.read("货币",message.author.id,"斯玛特","0"))
                    if 斯玛特 < Decimal(re.search("[0-9]+",message.content).group()):
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                        return 0
                    await data.write("货币",message.author.id,"斯玛特",str(斯玛特-Decimal(re.search("[0-9]+",message.content).group())))
                    await data.write("其他",message.author.id,"渔网投入",str(Decimal(await data.read("其他",message.author.id,"渔网投入","0"))+Decimal(re.search("[0-9]+",message.content).group())))
                if Decimal(await data.read("其他",message.author.id,"渔网投入","0")) >= Decimal(强化需求[yuw]):
                    await data.write("装备",message.author.id,"渔网",str(Decimal(yuw)+Decimal("1")))
                    await data.write("其他",message.author.id,"渔网投入",str(Decimal(await data.read("其他",message.author.id,"渔网投入","0"))-Decimal(强化需求[yuw])))
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 强化成功\r当前等级：{str(Decimal(yuw)+Decimal("1"))}')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}>\r投入金额：{await data.read("其他",message.author.id,"渔网投入","0")}/{强化需求[yuw]}\r输入：强化渔网+金额  渔网熔券+数量\r一张兑换券等价于100w斯玛特（仅此功能）')
            
            elif re.match("(渔|鱼){1}网 ?(融|熔){1}券 ?([0-9]+)",message.content) != None:
                yuw = await data.read("装备",message.author.id,"渔网","0")
                if yuw == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你还没有渔网呢')
                    return 0
                强化需求 = {"1":"500000","2":"1000000","3":"2000000","4":"3000000","5":"4000000","6":"5000000","7":"6000000","8":"7000000","9":"10000000"}
                if re.search("[0-9]+",message.content) != None:
                    兑换券 = Decimal(await data.read("物品",message.author.id,"兑换券","0"))
                    if 兑换券 < Decimal(re.search("[0-9]+",message.content).group()):
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换券不足')
                        return 0
                    await data.write("物品",message.author.id,"兑换券",str(兑换券-Decimal(re.search("[0-9]+",message.content).group())))
                    await data.write("其他",message.author.id,"渔网投入",str(Decimal(await data.read("其他",message.author.id,"渔网投入","0"))+Decimal("1000000")*Decimal(re.search("[0-9]+",message.content).group())))
                if Decimal(await data.read("其他",message.author.id,"渔网投入","0")) >= Decimal(强化需求[yuw]):
                    await data.write("装备",message.author.id,"渔网",str(Decimal(yuw)+Decimal("1")))
                    await data.write("其他",message.author.id,"渔网投入",str(Decimal(await data.read("其他",message.author.id,"渔网投入","0"))-Decimal(强化需求[yuw])))
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 强化成功\r当前等级：{str(Decimal(yuw)+Decimal("1"))}')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}>\r投入金额：{await data.read("其他",message.author.id,"渔网投入","0")}/{强化需求[yuw]}\r输入：强化渔网+金额  渔网熔券+数量\r一张兑换券等价于100w斯玛特（仅此功能）')
            
            #装备商店

            elif message.content == '装备商店':
                await self.api.post_message(channel_id=message.channel_id, content='''装备商店
[1级]小刀—20斯玛特|头盔—20斯玛特|钱袋—30斯玛特
[2级]小刀—80斯玛特|头盔—100斯玛特|钱袋—150斯玛特
[3级]小刀—110斯玛特|头盔—170斯玛特|钱袋—330斯玛特
[4级]小刀—150斯玛特|头盔—260斯玛特|钱袋—540斯玛特
[5级]小刀—240斯玛特|头盔—350斯玛特|钱袋—710斯玛特
[6级]小刀—350斯玛特|头盔—480斯玛特|钱袋—880斯玛特
[7级]小刀—490斯玛特|头盔—600斯玛特|钱袋—1130斯玛特
[8级]小刀—640斯玛特|头盔—780斯玛特|钱袋—1400斯玛特
[9级]小刀—888斯玛特|头盔—1222斯玛特|钱袋—1777斯玛特
小刀每级增加5%打劫成功率
头盔每级增加5%打劫反杀率
*小刀与头盔效果会抵消
钱袋每级增加打劫获取斯玛特下限1上限2
指令：买+商品
如：买1级小刀''')

            elif re.match("买 ?(1|2|3|4|5|6|7|8|9){1} ?级 ?(小刀|头盔|钱袋){1}",message.content) != None:
                name = re.search("(小刀|钱袋|头盔)",message.content).group()
                num = re.search("(1|2|3|4|5|6|7|8|9)",message.content).group()
                价格 = {"小刀":{"1":"20","2":"80","3":"110","4":"150","5":"240","6":"350","7":"490","8":"640","9":"888"},
                "头盔":{"1":"20","2":"100","3":"170","4":"260","5":"350","6":"480","7":"600","8":"780","9":"1222"},
                "钱袋":{"1":"30","2":"150","3":"330","4":"540","5":"710","6":"880","7":"1130","8":"1400","9":"1777"}
                }
                if Decimal(await data.read("装备",message.author.id,name,"0")) >= Decimal(num):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有更高级的{name}了')
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(价格[name][num]):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("装备",message.author.id,name,num)
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(价格[name][num])))
            
            elif re.match("打劫<@![0-9]+>",message.content) != None:
                time_dajie = float(await data.read("其他",message.mentions[0].id,"打劫时间","0"))
                time = Time.time()
                time_wait = 300
                if await data.read("装备",message.author.id,"RPG","0") == "1":
                    time_wait = time_wait / 3
                if message.mentions[0].id == "16804913220467607239":
                    time_wait = time_wait / 2.5
                if time - time_dajie < time_wait :
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 对方{int(time - time_dajie)}秒前已经被打劫了，饶了他吧')
                else:
                    斯玛特 = Decimal(await data.read("货币",message.mentions[0].id,"斯玛特","0"))+Decimal(await data.read("货币",message.mentions[0].id,"银行斯玛特","0"))
                    if 斯玛特 < 22:
                        await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 对方都没钱了，别打劫了')
                    else:
                        体力 = Decimal(await data.read("属性",message.author.id,"体力","100"))
                        if 体力 < 5:
                            await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 体力不支')
                        else:
                            await data.write("其他",message.mentions[0].id,"打劫时间",str(Time.time()))
                            rand1 = Decimal(random.randint(1,100))+Decimal(await data.read("装备",message.author.id,"小刀","0"))*Decimal("5")
                            rand2 = Decimal(random.randint(1,100))+Decimal(await data.read("装备",message.mentions[0].id,"头盔","0"))*Decimal("5")
                            sub_体力 = random.randint(2,5)
                            await data.属性操作(message.author.id,"体力",sub_体力,"sub")
                            if rand1 > rand2:
                                钱袋 = Decimal(await data.read("装备",message.author.id,"钱袋","0"))
                                add_斯玛特 = Decimal(random.randint(钱袋+Decimal(1),钱袋*Decimal(2)+Decimal(10)))
                                await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特",0))+add_斯玛特))
                                await data.write("货币",message.mentions[0].id,"斯玛特",str(Decimal(await data.read("货币",message.mentions[0].id,"斯玛特",0))-add_斯玛特))
                                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}>打劫了<@!{message.mentions[0].id}>\r成功打劫到{add_斯玛特}斯玛特\r降低{sub_体力}体力')
                            else:
                                钱袋 = Decimal(await data.read("装备",message.mentions[0].id,"钱袋","0"))
                                add_斯玛特 = Decimal(random.randint(钱袋+Decimal(1),钱袋*Decimal(2)+Decimal(10)))
                                await data.write("货币",message.mentions[0].id,"斯玛特",str(Decimal(await data.read("货币",message.mentions[0].id,"斯玛特",0))+add_斯玛特))
                                await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特",0))-add_斯玛特))
                                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}>打劫了<@!{message.mentions[0].id}>\r被对面反杀了！\r损失{add_斯玛特}斯玛特\r降低{sub_体力}体力')

            #农具商店

            elif message.content == '农具商店':
                await self.api.post_message(channel_id=message.channel_id, content='''农具商店
大容量水壶：88斯玛特
*种植时消耗体力减少33%
军用铲子：88斯玛特
*收获时消耗体力减少33%
上古农书：其他方式获取
*收获时作物增量0～5%
输入"买+物品"购买''')

            elif re.match("买 ?(大容量水壶|军用铲子){1}",message.content) != None:
                name = re.search("(大容量水壶|军用铲子)",message.content).group()
                if await data.read("装备",message.author.id,name,"0") == "1":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有{name}了')
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal("88"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("装备",message.author.id,name,"1")
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal("88")))

            #婚戒商店

            elif message.content == '婚戒商店':
                await self.api.post_message(channel_id=message.channel_id, content='''婚戒商店
镀金戒指一对:520斯玛特
黄金戒指一对:1314斯玛特
钻石戒指一对:5200斯玛特
红宝石戒指一对:13520斯玛特
输入 买+戒指名【会覆盖已买戒指】''')
                
            elif re.match("买 ?(镀金|黄金|钻石|红宝石){1} ?戒指",message.content) != None:
                name = re.search("(镀金|黄金|钻石|红宝石)",message.content).group()
                name_num = {"镀金":"1","黄金":"2","钻石":"3","红宝石":"4"}
                name_price = {"镀金":"520","黄金":"1314","钻石":"5200","红宝石":"13520"}
                if Decimal(await data.read("装备",message.author.id,"戒指","0")) >= Decimal(name_num[name]):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有更高级的戒指了')
                    return 0
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(name_price[name]):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("装备",message.author.id,"戒指",name_num[name])
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(name_price[name])))

            #兑换商店

            elif message.content == '兑换商店':
                await self.api.post_message(channel_id=message.channel_id, content=f'''兑换商店
您当前有{await data.read("物品",message.author.id,"兑换券","0")}张兑换券
[装备]鱼吸引器（1券）：鱼上钩速度提高20％
[装备]声呐（3券+鱼吸引器）：高科技产物，鱼上钩速度提高50％
[装备]多功能锄（1券）：农场体力消耗减少20％
[装备]RPG（3券）：打劫等待时间降至100秒
[礼包]属性礼包1（1券,限购1）：10精力上限+10体力上限+2千斯玛特+全部属性恢复50％{await data.read("其他",message.author.id,"属性礼包1","'{你可兑换}'")}
[礼包]属性礼包2（2券,限购1）：20精力上限+25体力上限+5千斯玛特+全部属性完全恢复{await data.read("其他",message.author.id,"属性礼包2","'{你可兑换}'")}
————
输入"兑换+商品"兑换''')

            elif re.match("(买|兑换){1} ?(鱼吸引器|多功能锄)",message.content) != None:
                name = re.search("(鱼吸引器|多功能锄)",message.content).group()
                if Decimal(await data.read("装备",message.author.id,name,"0")) >= Decimal("1"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有{name}了')
                    return 0
                if Decimal(await data.read("物品",message.author.id,"兑换券","0"))<Decimal("1"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换券不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换成功')
                    await data.write("装备",message.author.id,name,"1")
                    await data.write("物品",message.author.id,"兑换券",str(Decimal(await data.read("物品",message.author.id,"兑换券","0"))-Decimal("1")))

            elif re.match("(买|兑换){1} ?声呐",message.content) != None:
                if Decimal(await data.read("装备",message.author.id,"鱼吸引器","0")) < Decimal("1"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你还没有鱼吸引器呢')
                    return 0
                if Decimal(await data.read("装备",message.author.id,"鱼吸引器","0")) >= Decimal("2"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有声呐了')
                    return 0
                if Decimal(await data.read("物品",message.author.id,"兑换券","0"))<Decimal("3"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换券不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换成功')
                    await data.write("装备",message.author.id,"鱼吸引器","2")
                    await data.write("物品",message.author.id,"兑换券",str(Decimal(await data.read("物品",message.author.id,"兑换券","0"))-Decimal("3")))

            elif re.match("(买|兑换){1} ?(r|R){1} ?(p|P){1} ?(g|G){1}",message.content) != None:
                if Decimal(await data.read("装备",message.author.id,"RPG","0")) >= Decimal("1"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经有RPG了')
                    return 0
                if Decimal(await data.read("物品",message.author.id,"兑换券","0"))<Decimal("3"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换券不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换成功')
                    await data.write("装备",message.author.id,"RPG","1")
                    await data.write("物品",message.author.id,"兑换券",str(Decimal(await data.read("物品",message.author.id,"兑换券","0"))-Decimal("3")))

            elif re.match("(买|兑换){1} ?属性礼包 ?(1|一){1}",message.content) != None:
                if await data.read("其他",message.author.id,"属性礼包1","'{你可兑换}'") == '{你不可兑换}':
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经兑换过这个礼包了')
                    return 0
                if Decimal(await data.read("物品",message.author.id,"兑换券","0"))<Decimal("1"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换券不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换成功')
                    await data.write("其他",message.author.id,"属性礼包1","'{你不可兑换}'")
                    await data.write("属性",message.author.id,"体力上限",str(Decimal(await data.read("属性",message.author.id,"体力上限","100"))+Decimal("10")))
                    await data.write("属性",message.author.id,"精力上限",str(Decimal(await data.read("属性",message.author.id,"精力上限","100"))+Decimal("10")))
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))+Decimal("2000")))
                    await data.属性操作(message.author.id,"精力",Decimal(await data.read("属性",message.author.id,"精力上限","100"))/Decimal("2"),"add")
                    await data.属性操作(message.author.id,"体力",Decimal(await data.read("属性",message.author.id,"体力上限","100"))/Decimal("2"),"add")
                    await data.write("物品",message.author.id,"兑换券",str(Decimal(await data.read("物品",message.author.id,"兑换券","0"))-Decimal("1")))
                
            elif re.match("(买|兑换){1} ?属性礼包 ?(2|二){1}",message.content) != None:
                if await data.read("其他",message.author.id,"属性礼包2","'{你可兑换}'") == '{你不可兑换}':
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你已经兑换过这个礼包了')
                    return 0
                if Decimal(await data.read("物品",message.author.id,"兑换券","0"))<Decimal("2"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换券不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 兑换成功')
                    await data.write("其他",message.author.id,"属性礼包2","'{你不可兑换}'")
                    await data.write("属性",message.author.id,"体力上限",str(Decimal(await data.read("属性",message.author.id,"体力上限","100"))+Decimal("25")))
                    await data.write("属性",message.author.id,"精力上限",str(Decimal(await data.read("属性",message.author.id,"精力上限","100"))+Decimal("20")))
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))+Decimal("5000")))
                    await data.属性操作(message.author.id,"精力",Decimal(await data.read("属性",message.author.id,"精力上限","100")),"add")
                    await data.属性操作(message.author.id,"体力",Decimal(await data.read("属性",message.author.id,"体力上限","100")),"add")
                    await data.write("物品",message.author.id,"兑换券",str(Decimal(await data.read("物品",message.author.id,"兑换券","0"))-Decimal("2")))
                    
            #头衔商店

            elif message.content == '头衔商店':
                await self.api.post_message(channel_id=message.channel_id, content='''头衔商店
「小有所成Lv.1」— 100斯玛特
「小有所成Lv.2」— 500斯玛特
「小有所成Lv.3」— 2000斯玛特
「富可敌城Lv.4」— 1w斯玛特
「富可敌城Lv.5」— 2w斯玛特
「富可敌城Lv.6」— 5w斯玛特
「富甲一方Lv.7」— 10w斯玛特
「富甲一方Lv.8」— 20w斯玛特
「富甲一方Lv.9」— 30w斯玛特
「富可敌国MAX」— 100w斯玛特
输入 买头衔 等级(MAX填10)
例如 买头衔 10''')
                
            elif re.match("买头衔 ?(1|2|3|4|5|6|9|10){1}",message.content) != None:
                num = re.search("[0-9]+",message.content).group()
                头衔价格 = {"1":"100","2":"500","3":"2000","4":"10000","5":"20000","6":"50000","7":"100000","8":"200000","9":"300000","10":"1000000"}
                头衔 = {"1":"小有所成Lv.1","2":"小有所成Lv.2","3":"小有所成Lv.3","4":"富可敌城Lv.4","5":"富可敌城Lv.5","6":"富可敌城Lv.6","7":"富甲一方Lv.7","8":"富甲一方Lv.8","9":"富甲一方Lv.9","10":"富可敌国MAX"}
                if Decimal(await data.read("货币",message.author.id,"斯玛特","0"))<Decimal(头衔价格[num]):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 斯玛特不足')
                else:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 购买成功')
                    await data.write("属性",message.author.id,"财富头衔",f"'{头衔[num]}'")
                    await data.write("货币",message.author.id,"斯玛特",str(Decimal(await data.read("货币",message.author.id,"斯玛特","0"))-Decimal(头衔价格[num])))

            #农场

            elif message.content == "农场":
                await self.api.post_message(channel_id=message.channel_id, content=f'🌻种子商店\r🌻种子库存\r🌻我的农场\r🌻我的仓库\r🌻收获/铲除/查时间+作物名\r🌻买种子/种植/出售+作物名+数量\r🌻作物图鉴\r🚜扩充地块\r💵兑斯玛特+数量(35:1)')

            elif message.content == "作物图鉴":
                await self.api.post_message(channel_id=message.channel_id, content=f'''┌────────────
├⛳️[品种][价格][时间][利润][售价]
├🥬白菜├5├5├2├7
├🍅番茄├10├8├4├14
├🌽玉米├20├10├6├26
├🥜花生├40├15├10├50
├🍉西瓜├60├30├22├82
├🍓草莓├80├45├35├115
├🍑桃子├100├50├41├141
├🍎苹果├150├60├52├202
├🍍菠萝├300├90├81├381
├🍡西方团子├1├1├1├2
├🥝锁喉桃├9├7├4├13
├🍏道理果├27├15├10├37
├🥔野生榴莲├731├234├211├942
├🎃南蛮大瓜├1000├500├234├1234''')

            elif message.content == "种子商店":
                await self.api.post_message(channel_id=message.channel_id, content=f"""┌种子商店
├────────────
├⛳️[品种][价格][时间]
├🥬白菜├7├5
├🍅番茄├14├8
├🌽玉米├26├10
├🥜花生├50├15
├🍉西瓜├82├30
├🍓草莓├115├45
├🍑桃子├141├50
├🍎苹果├202├60
├🍍菠萝├381├90
├🍡西方团子├2├1
├🥝锁喉桃├15├7
├🍏道理果├37├15
├🥔野生榴莲├942├234
├🎃南蛮大瓜├1234├500
├────────────
├发送相关命令
├例如:买种子 白菜 数量
└────────────""")

            elif message.content == "种子库存":
                seed = await data.read("农场",message.author.id,"作物种子",'''"{'白菜':0,'番茄':0,'玉米':0,'西瓜':0,'花生':0,'草莓':0,'桃子':0,'苹果':0,'菠萝':0,'西方团子':0,'锁喉桃':0,'道理果':0,'野生榴莲':0,'南蛮大瓜':0}"''')
                seed = eval(seed)
                await self.api.post_message(channel_id=message.channel_id, content=f"""┌{message.author.username}的种子仓库
├────────────
├🥬白菜:{seed["白菜"]}
├🍅番茄:{seed["番茄"]}
├🌽玉米:{seed["玉米"]}
├🥜花生:{seed["花生"]}
├🍉西瓜:{seed["西瓜"]}
├🍓草莓:{seed["草莓"]}
├🍑桃子:{seed["桃子"]}
├🍎苹果:{seed["苹果"]}
├🍍菠萝:{seed["菠萝"]}
├🍡西方团子:{seed["西方团子"]}
├🥝锁喉桃:{seed["锁喉桃"]}
├🍏道理果:{seed["道理果"]}
├🥔野生榴莲:{seed["野生榴莲"]}
├🎃南蛮大瓜:{seed["南蛮大瓜"]}
├────────────
├发送相关命令种植
├如"种植 白菜 1"
└────────────""")

            elif message.content == "我的农场":
                plants = await data.read("农场",message.author.id,"作物",'''"{'白菜':['0','0'],'番茄':['0','0'],'玉米':['0','0'],'西瓜':['0','0'],'花生':['0','0'],'草莓':['0','0'],'桃子':['0','0'],'苹果':['0','0'],'菠萝':['0','0'],'西方团子':['0','0'],'锁喉桃':['0','0'],'道理果':['0','0'],'野生榴莲':['0','0'],'南蛮大瓜':['0','0']}"''')
                plants = eval(plants)
                await self.api.post_message(channel_id=message.channel_id, content=f"""┌{message.author.username}的种子仓库
├────────────
├🥬白菜:{await self.作物状态(plants,"白菜")}
├🍅番茄:{await self.作物状态(plants,"番茄")}
├🌽玉米:{await self.作物状态(plants,"玉米")}
├🥜花生:{await self.作物状态(plants,"花生")}
├🍉西瓜:{await self.作物状态(plants,"西瓜")}
├🍓草莓:{await self.作物状态(plants,"草莓")}
├🍑桃子:{await self.作物状态(plants,"桃子")}
├🍎苹果:{await self.作物状态(plants,"苹果")}
├🍍菠萝:{await self.作物状态(plants,"菠萝")}
├🍡西方团子:{await self.作物状态(plants,"西方团子")}
├🥝锁喉桃:{await self.作物状态(plants,"锁喉桃")}
├🍏道理果:{await self.作物状态(plants,"道理果")}
├🥔野生榴莲:{await self.作物状态(plants,"野生榴莲")}
├🎃南蛮大瓜:{await self.作物状态(plants,"南蛮大瓜")}
├────────────
├总面积:{await data.read("农场",message.author.id,"面积","30")}
├剩余面积:{Decimal(await data.read("农场",message.author.id,"面积","30"))-Decimal(plants["白菜"][0])-Decimal(plants["番茄"][0])-Decimal(plants["玉米"][0])-Decimal(plants["花生"][0])-Decimal(plants["西瓜"][0])-Decimal(plants["草莓"][0])-Decimal(plants["桃子"][0])-Decimal(plants["苹果"][0])-Decimal(plants["菠萝"][0])-Decimal(plants["西方团子"][0])-Decimal(plants["锁喉桃"][0])-Decimal(plants["道理果"][0])-Decimal(plants["野生榴莲"][0])-Decimal(plants["南蛮大瓜"][0])}
└────────────""")

            elif message.content == "我的仓库":
                fruit = await data.read("农场",message.author.id,"作物果实",'''"{'白菜':0,'番茄':0,'玉米':0,'西瓜':0,'花生':0,'草莓':0,'桃子':0,'苹果':0,'菠萝':0,'西方团子':0,'锁喉桃':0,'道理果':0,'野生榴莲':0,'南蛮大瓜':0}"''')
                fruit = eval(fruit)
                await self.api.post_message(channel_id=message.channel_id, content=f"""┌{message.author.username}的作物仓库
├────────────
├🥬白菜:{fruit["白菜"]}
├🍅番茄:{fruit["番茄"]}
├🌽玉米:{fruit["玉米"]}
├🥜花生:{fruit["花生"]}
├🍉西瓜:{fruit["西瓜"]}
├🍓草莓:{fruit["草莓"]}
├🍑桃子:{fruit["桃子"]}
├🍎苹果:{fruit["苹果"]}
├🍍菠萝:{fruit["菠萝"]}
├🍡西方团子:{fruit["西方团子"]}
├🥝锁喉桃:{fruit["锁喉桃"]}
├🍏道理果:{fruit["道理果"]}
├🥔野生榴莲:{fruit["野生榴莲"]}
├🎃南蛮大瓜:{fruit["南蛮大瓜"]}
├────────────
├发送相关命令出售
├如"出售 白菜 1"
└────────────""")

            elif message.content == "扩充地块":
                地块 = Decimal(await data.read("农场",message.author.id,"面积","30"))
                if 地块 > Decimal("69"):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的地块已经达到上限')
                    return 0
                农场币 = Decimal(await data.read("货币",message.author.id,"农场币","20"))
                农场币_cost = (地块+Decimal("30"))*Decimal("15")
                if 农场币 <= 农场币_cost:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 农场币不足，扩充地块需要{农场币_cost}(+1)农场币')
                    return 0
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 扩充成功')
                await data.write("农场",message.author.id,"面积",str(地块+Decimal("1")))
                await data.write("货币",message.author.id,"农场币",str(农场币-农场币_cost))

            elif re.match("买 ?种子 ?(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜){1} ?([0-9]+)",message.content):
                plant = re.search("(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜)",message.content).group()
                num = re.search("[0-9]+",message.content).group()
                price = {"白菜":"5","番茄":"10","玉米":"20","花生":"40","西瓜":"60","草莓":"80","桃子":"100","苹果":"150","菠萝":"300","西方团子":"1","锁喉桃":"9","道理果":"27","野生榴莲":"731","南蛮大瓜":"1000"}
                农场币_cost = Decimal(price[plant]) * Decimal(num)
                农场币 = Decimal(await data.read("货币",message.author.id,"农场币","20"))
                if 农场币 < 农场币_cost:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 农场币不足，需要{农场币_cost}农场币')
                    return 0
                await data.write("货币",message.author.id,"农场币",str(农场币-农场币_cost))
                seed = await data.read("农场",message.author.id,"作物种子",'''"{'白菜':0,'番茄':0,'玉米':0,'西瓜':0,'花生':0,'草莓':0,'桃子':0,'苹果':0,'菠萝':0,'西方团子':0,'锁喉桃':0,'道理果':0,'野生榴莲':0,'南蛮大瓜':0}"''')
                seed = eval(seed)
                seed[plant] = str(Decimal(seed[plant])+Decimal(num))
                await data.write("农场",message.author.id,"作物种子",f'''"{seed}"''')
                await self.api.post_message(channel_id=message.channel_id, content=f'''┌购买种子
├──────
├农工:{message.author.username}
├物品:{plant}
├消费:{农场币_cost}
├余额:{str(农场币-农场币_cost)}
├查看“种子库存”
└──────''')

            elif re.match("(种|种植){1} ?(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜){1} ?([0-9]+)",message.content):
                plant = re.search("(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜)",message.content).group()
                num = re.search("[0-9]+",message.content).group()
                if num == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 种植数量不能为0')
                    return 0
                体力 = Decimal(await data.read("属性",message.author.id,"体力","100"))
                体力_sub = Decimal(num) / Decimal("4")
                if await data.read("装备",message.author.id,"大容量水壶","0") == "1":
                    体力_sub = 体力_sub / Decimal("3") * Decimal("2")
                if await data.read("装备",message.author.id,"多功能锄","0") == "1":
                    体力_sub = 体力_sub * Decimal("0.8")
                if 体力 < 体力_sub:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 体力不支')
                    return 0
                seed = await data.read("农场",message.author.id,"作物种子",'''"{'白菜':0,'番茄':0,'玉米':0,'西瓜':0,'花生':0,'草莓':0,'桃子':0,'苹果':0,'菠萝':0,'西方团子':0,'锁喉桃':0,'道理果':0,'野生榴莲':0,'南蛮大瓜':0}"''')
                seed = eval(seed)
                if Decimal(seed[plant]) < Decimal(num):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的{plant}种子不足')
                    return 0
                plants = await data.read("农场",message.author.id,"作物",'''"{'白菜':['0','0'],'番茄':['0','0'],'玉米':['0','0'],'西瓜':['0','0'],'花生':['0','0'],'草莓':['0','0'],'桃子':['0','0'],'苹果':['0','0'],'菠萝':['0','0'],'西方团子':['0','0'],'锁喉桃':['0','0'],'道理果':['0','0'],'野生榴莲':['0','0'],'南蛮大瓜':['0','0']}"''')
                plants = eval(plants)
                面积 = Decimal(await data.read("农场",message.author.id,"面积","30"))
                面积_use = Decimal(plants["白菜"][0])+Decimal(plants["番茄"][0])+Decimal(plants["玉米"][0])+Decimal(plants["花生"][0])+Decimal(plants["西瓜"][0])+Decimal(plants["草莓"][0])+Decimal(plants["桃子"][0])+Decimal(plants["苹果"][0])+Decimal(plants["菠萝"][0])+Decimal(plants["西方团子"][0])+Decimal(plants["锁喉桃"][0])+Decimal(plants["道理果"][0])+Decimal(plants["野生榴莲"][0])+Decimal(plants["南蛮大瓜"][0])
                if 面积-面积_use < Decimal(num):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的农场已经种不下了，剩余面积{str(面积-面积_use)}')
                    return 0
                if plants[plant][0] != "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的农场已经种植{plant}了')
                    return 0
                costtime = {"白菜":"300","番茄":"480","玉米":"600","花生":"900","西瓜":"1800","草莓":"2700","桃子":"3000","苹果":"3600","菠萝":"5400","西方团子":"60","锁喉桃":"420","道理果":"900","野生榴莲":"14040","南蛮大瓜":"30000"}
                seed[plant] = str(Decimal(seed[plant])-Decimal(num))
                await data.write("农场",message.author.id,"作物种子",f'''"{seed}"''')
                plants[plant] = [str(num),str(Time.time()+float(costtime[plant]))]
                await data.write("农场",message.author.id,"作物",f'''"{plants}"''')
                await self.api.post_message(channel_id=message.channel_id, content=f'''┌种植{plant}
├──────
├农工:{message.author.username}
├种植{plant}:{num}颗
├{await data.属性操作(message.author.id,"体力",体力_sub,"sub")}
├收获时间:{Decimal(costtime[plant])/Decimal("60")}分钟收获
└──────''')

            elif re.match("(卖|出售){1} ?(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜){1} ?([0-9]+)",message.content):
                plant = re.search("(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜)",message.content).group()
                num = re.search("[0-9]+",message.content).group()
                if num == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 出售数量不能为0')
                    return 0
                price = {"白菜":"7","番茄":"14","玉米":"26","花生":"50","西瓜":"82","草莓":"115","桃子":"141","苹果":"202","菠萝":"381","西方团子":"2","锁喉桃":"15","道理果":"37","野生榴莲":"942","南蛮大瓜":"1234"}
                fruit = await data.read("农场",message.author.id,"作物果实",'''"{'白菜':0,'番茄':0,'玉米':0,'西瓜':0,'花生':0,'草莓':0,'桃子':0,'苹果':0,'菠萝':0,'西方团子':0,'锁喉桃':0,'道理果':0,'野生榴莲':0,'南蛮大瓜':0}"''')
                fruit = eval(fruit)
                if Decimal(num) > Decimal(fruit[plant]):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> {plant}库存不足')
                    return 0
                fruit[plant] = str(Decimal(fruit[plant])-Decimal(num))
                await data.write("农场",message.author.id,"作物果实",f'''"{fruit}"''')
                农场币 = Decimal(await data.read("货币",message.author.id,"农场币","20"))
                农场币_add = Decimal(price[plant])*Decimal(num)
                await data.write("货币",message.author.id,"农场币",str(农场币 + 农场币_add))
                await self.api.post_message(channel_id=message.channel_id, content=f'''┌出售果实
├──────
├农工:{message.author.username}
├物品:{plant}
├收益:{农场币_add}
├余额:{str(农场币 + 农场币_add)}
└──────''')

            elif re.match("(收|收获){1} ?(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜){1}",message.content):
                plant = re.search("(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜)",message.content).group()
                plants = await data.read("农场",message.author.id,"作物",'''"{'白菜':['0','0'],'番茄':['0','0'],'玉米':['0','0'],'西瓜':['0','0'],'花生':['0','0'],'草莓':['0','0'],'桃子':['0','0'],'苹果':['0','0'],'菠萝':['0','0'],'西方团子':['0','0'],'锁喉桃':['0','0'],'道理果':['0','0'],'野生榴莲':['0','0'],'南蛮大瓜':['0','0']}"''')
                plants = eval(plants)
                if plants[plant][0] == '0':
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的农场里没有种植{plant}')
                    return 0
                if await self.作物状态(plants,plant) == "未成熟":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你农场里的{plant}还没成熟')
                    return 0
                体力 = Decimal(await data.read("属性",message.author.id,"体力","100"))
                体力_sub = Decimal(plants[plant][0]) / Decimal("4")
                if await data.read("装备",message.author.id,"军用铲子","0") == "1":
                    体力_sub = 体力_sub / Decimal("3") * Decimal("2")
                if await data.read("装备",message.author.id,"多功能锄","0") == "1":
                    体力_sub = 体力_sub * Decimal("0.8")
                if 体力 < 体力_sub:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 体力不支')
                    return 0
                plant_get = Decimal(plants[plant][0])
                if await data.read("装备",message.author.id,"上古农书","0") == "1":
                    plant_get = (plant_get * (Decimal('100')+Decimal(random.randint(0,5))) / Decimal('100')).quantize(Decimal('0.'))
                plants[plant] = ['0','0']
                await data.write("农场",message.author.id,"作物",f'''"{plants}"''')
                fruit = await data.read("农场",message.author.id,"作物果实",'''"{'白菜':0,'番茄':0,'玉米':0,'西瓜':0,'花生':0,'草莓':0,'桃子':0,'苹果':0,'菠萝':0,'西方团子':0,'锁喉桃':0,'道理果':0,'野生榴莲':0,'南蛮大瓜':0}"''')
                fruit = eval(fruit)
                fruit[plant] = str(Decimal(fruit[plant])+plant_get)
                await data.write("农场",message.author.id,"作物果实",f'''"{fruit}"''')
                await self.api.post_message(channel_id=message.channel_id, content=f'''┌收获{plant}
├──────
├农工:{message.author.username}
├收获{plant}:{plant_get}颗
├{await data.属性操作(message.author.id,"体力",体力_sub,"sub")}
├仓库总数:{fruit[plant]}
└──────''')

            elif re.match("查 ?(时间)? ?(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜){1}",message.content):
                plant = re.search("(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜)",message.content).group()
                plants = await data.read("农场",message.author.id,"作物",'''"{'白菜':['0','0'],'番茄':['0','0'],'玉米':['0','0'],'西瓜':['0','0'],'花生':['0','0'],'草莓':['0','0'],'桃子':['0','0'],'苹果':['0','0'],'菠萝':['0','0'],'西方团子':['0','0'],'锁喉桃':['0','0'],'道理果':['0','0'],'野生榴莲':['0','0'],'南蛮大瓜':['0','0']}"''')
                plants = eval(plants)
                if plants[plant][0] == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的农场里没有种植{plant}')
                    return 0
                if Decimal(plants[plant][1]) <= Decimal(Time.time()):
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你农场里的{plant}已经成熟了')
                    return 0
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你农场里的{plant}还有{(Decimal(plants[plant][1]) - Decimal(Time.time())).quantize(Decimal("0."))}秒成熟')

            elif re.match("(铲|铲除){1} ?(作物)? ?(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜){1}",message.content):
                plant = re.search("(白菜|番茄|玉米|花生|西瓜|草莓|桃子|苹果|菠萝|西方团子|锁喉桃|道理果|野生榴莲|南蛮大瓜)",message.content).group()
                plants = await data.read("农场",message.author.id,"作物",'''"{'白菜':['0','0'],'番茄':['0','0'],'玉米':['0','0'],'西瓜':['0','0'],'花生':['0','0'],'草莓':['0','0'],'桃子':['0','0'],'苹果':['0','0'],'菠萝':['0','0'],'西方团子':['0','0'],'锁喉桃':['0','0'],'道理果':['0','0'],'野生榴莲':['0','0'],'南蛮大瓜':['0','0']}"''')
                plants = eval(plants)
                if plants[plant][0] == "0":
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你的农场里没有种植{plant}')
                    return 0
                plants[plant] = ['0','0']
                await data.write("农场",message.author.id,"作物",f'''"{plants}"''')
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 铲除成功')

            
            #装备系统
            elif re.match(r"发行(.*) (.*) (.*) ([0-9]+)", message.content) != None:
                if message.author.id != 11782375117980851014:
                    await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 你没有权限')
                    return 0
                type = re.match(r"(.*) (.*) (.*) ([0-9]+)", message.content).group(1)
                name = re.match(r"(.*) (.*) (.*) ([0-9]+)", message.content).group(2)
                color = re.match(r"(.*) (.*) (.*) ([0-9]+)", message.content).group(3)
                num = re.match(r"(.*) (.*) (.*) ([0-9]+)", message.content).group(4)
                no = str(await data.read("装备库","0","发行数量","0"))
                no = str(no + 1)
                await data.write("装备库","0","发行数量",no)
                await data.write("装备库",no,"名字",name)
                await data.write("装备库",no,"类型",type)
                await data.write("装备库",no,"颜色",color)
                await data.write("装备库",no,"数量",num)
                await self.api.post_message(channel_id=message.channel_id, content=f'<@!{message.author.id}> 发行成功')
                
                



    async def 作物状态(self,plants,plants_name):
        if plants[plants_name][0] == "0":
            return "未种植"
        if Decimal(plants[plants_name][1]) <= Decimal(Time.time()):
            return "已成熟"
        return "未成熟"

    async def 上钩(self,author_id):
        经验 = Decimal(await data.read("属性",author_id,"经验","0"))
        鱼竿 = Decimal(await data.read("装备",author_id,"鱼竿","0"))
        斯玛特 = Decimal(await data.read("货币",author_id,"斯玛特","0"))
        鱼 = Decimal(await data.read("数据",author_id,"鱼","0"))
        all鱼 = Decimal(await data.read("数据",author_id,"鱼","0"))
        钓鱼次数 = Decimal(await data.read("数据",author_id,"钓鱼次数","0"))
        add_经验 = Decimal("10")
        tfl = Decimal(await data.read("天赋",author_id,"经验天赋1","0"))*5/10+1
        add_经验 = add_经验*tfl
        add_斯玛特_max = int(Decimal("2")*min(Decimal("9"),鱼竿)+Decimal("7")+max(Decimal("0"),鱼竿-Decimal("9")))
        add_斯玛特_min = int(min(Decimal("9"),鱼竿)+Decimal("4")+Decimal("0.5")*max(Decimal("0"),鱼竿-Decimal("9")))
        add_斯玛特 = Decimal(str(random.randint(add_斯玛特_min,add_斯玛特_max)))
        称 = "恭喜"
        后称 = "斯玛特"
        #附魔效果开始
        fm = "海之眷顾"
        yfm = await data.read("装备",author_id,"鱼竿附魔","[]")
        level =yfm.find(fm)
        if level !=-1:
            level = int(yfm[level + len(fm)])
            fmxg = eval(await data.read("附魔",fm,"各级效果","0"))
            print(fmxg)
            fmxg = int(fmxg[level-1])
            print(level)
            print(fmxg)
            if random.randint(0,999)<int(fmxg):
                pxs=int(await data.read("物品",author_id,"破限石","0"))
                pxs=pxs+1
                await data.write("物品",author_id,"破限石",str(pxs))
                后称 = "斯玛特{掉落一个破限石"+"}"
        #附魔效果结束
        if random.randint(0,999)==114:
            book = await data.read("物品", author_id, "附魔书", "[['空书'],['0']]")
            book = eval(book)
            if "空书" in book[0]:
                row = book[0].index("空书")
                value = int(book[1][row])
            else:
                book[0].append("空书")
                book[1].append("0")
                row = book[0].index("空书")
                value = 0
            book[1][row] = str(value + 1)
            await data.write("物品", author_id, "附魔书", str(book))  
            后称 = 后称 + "{掉落一本附魔书"+"}"
        if random.randint(0,99)<5*int(await data.read("天赋",author_id,"渔民天赋2","0")):
            称 = "۞鱼王۞恭喜"
            add_经验 = 5*add_经验
            add_斯玛特 = 2*add_斯玛特
        if await data.read("村庄_村民",author_id,"归属村庄","0") != "0":
            村钓 = str(Decimal(await data.read("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",'0'))+1)
            await data.write("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",村钓)
            贡献 = str(Decimal(await data.read("村庄_村民",author_id,"村庄贡献",'0'))+1)
            await data.write("村庄_村民",author_id,"村庄贡献",贡献)
        GodB = await data.read("其他",author_id,"量子之海","0")
        if GodB == "1":
            add_斯玛特=2*add_斯玛特
            add_经验=2*add_经验
            钓鱼次数=钓鱼次数+1
            鱼=鱼+1
            if await data.read("村庄_村民",author_id,"归属村庄","0") != "0":
                村钓 = str(Decimal(await data.read("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",'0'))+1)
                await data.write("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",村钓)
                贡献 = str(Decimal(await data.read("村庄_村民",author_id,"村庄贡献",'0'))+1)
                await data.write("村庄_村民",author_id,"村庄贡献",贡献)
        GodC = await data.read("其他",author_id,"海的女儿","0")
        if GodC == "1" and random.randint(0,99)<50:
            add_斯玛特=2*add_斯玛特
            add_经验=2*add_经验
            钓鱼次数=钓鱼次数+1
            鱼=鱼+1
            称 = "[海之女儿]发动：" + 称
            if await data.read("村庄_村民",author_id,"归属村庄","0") != "0":
                村钓 = str(Decimal(await data.read("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",'0'))+1)
                await data.write("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",村钓)
                贡献 = str(Decimal(await data.read("村庄_村民",author_id,"村庄贡献",'0'))+1)
                await data.write("村庄_村民",author_id,"村庄贡献",贡献)
        fm = "戒律·深罪之槛"
        yfm = await data.read("装备",author_id,"鱼竿附魔","[]")
        level =yfm.find(fm)
        if level !=-1:
            add_斯玛特=3*add_斯玛特
            add_经验=3*add_经验
            钓鱼次数=钓鱼次数+2
            鱼=鱼+2
            if await data.read("村庄_村民",author_id,"归属村庄","0") != "0":
                村钓 = str(Decimal(await data.read("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",'0'))+2)
                await data.write("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",村钓)
                贡献 = str(Decimal(await data.read("村庄_村民",author_id,"村庄贡献",'0'))+2)
                await data.write("村庄_村民",author_id,"村庄贡献",贡献)
                    
        fm = "黄金·璀璨之歌"
        yfm = await data.read("装备",author_id,"鱼竿附魔","[]")
        level =yfm.find(fm)
        if level !=-1:
            add_斯玛特=3*add_斯玛特
            add_经验=3*add_经验
            钓鱼次数=钓鱼次数+2
            鱼=鱼+2
            if await data.read("村庄_村民",author_id,"归属村庄","0") != "0":
                村钓 = str(Decimal(await data.read("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",'0'))+2)
                await data.write("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",村钓)
                贡献 = str(Decimal(await data.read("村庄_村民",author_id,"村庄贡献",'0'))+2)
                await data.write("村庄_村民",author_id,"村庄贡献",贡献)
                    
        fm = "繁星·绘世之卷"
        yfm = await data.read("装备",author_id,"鱼竿附魔","[]")
        level =yfm.find(fm)
        if level !=-1:
            add_斯玛特=3*add_斯玛特
            add_经验=3*add_经验
            钓鱼次数=钓鱼次数+2
            鱼=鱼+2
            if await data.read("村庄_村民",author_id,"归属村庄","0") != "0":
                村钓 = str(Decimal(await data.read("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",'0'))+2)
                await data.write("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",村钓)
                贡献 = str(Decimal(await data.read("村庄_村民",author_id,"村庄贡献",'0'))+2)
                await data.write("村庄_村民",author_id,"村庄贡献",贡献)
        #附魔效果开始
        fm = "海之后裔"
        yfm = await data.read("装备",author_id,"鱼竿附魔","[]")
        level =yfm.find(fm)
        if level !=-1:
            level = int(yfm[level + len(fm)])
            fmxg = eval(await data.read("附魔",fm,"各级效果","0"))
            print(fmxg)
            fmxg = int(fmxg[level-1])
            print(level)
            print(fmxg)
            if random.randint(0,99)<int(fmxg):
                add_斯玛特=2*add_斯玛特
                add_经验=2*add_经验
                钓鱼次数=钓鱼次数+1
                鱼=鱼+1
                称 = "[海之后裔]发动：" + 称
                if await data.read("村庄_村民",author_id,"归属村庄","0") != "0":
                    村钓 = str(Decimal(await data.read("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",'0'))+1)
                    await data.write("村庄",await data.read("村庄_村民",author_id,"归属村庄","0"),"钓鱼次数",村钓)
                    贡献 = str(Decimal(await data.read("村庄_村民",author_id,"村庄贡献",'0'))+1)
                    await data.write("村庄_村民",author_id,"村庄贡献",贡献)
        #附魔效果结束
        if await data.read("村庄_村民", author_id, "归属村庄","0") != "0":
            village = await data.read("村庄_村民", author_id, "归属村庄","0")
            if await data.read("村庄", village, "参加情况","0") != "0":
                x = int(await data.read("村庄_村民", author_id, "村x",await data.read("村庄", village, "初始x","0")))
                y = int(await data.read("村庄_村民", author_id, "村y",await data.read("村庄", village, "初始y","0")))
                map = await data.read("四色战争地图", "0", "地块类型","0")
                map = eval(map)
                qu = map[x][y]
                if qu=="资源":
                    vf = Decimal(await data.read("村庄_仓库",village,"鱼","0"))
                    vjf = Decimal(await data.read("数据",author_id,"鱼","0"))
                    vjf = vjf-all鱼+1
                    vf = vf+vjf
                    vf = str(vf)
                    await data.write("村庄_仓库",village,"鱼",vf)
        await data.write("属性",author_id,"经验",str(经验+add_经验))
        await data.write("货币",author_id,"斯玛特",str(斯玛特+add_斯玛特))
        await data.write("数据",author_id,"鱼",str(鱼+Decimal("1")))
        await data.write("数据",author_id,"钓鱼次数",str(钓鱼次数+Decimal("1")))
        fish1 = ["来势汹汹的","张牙舞爪的","正在发呆的","可可爱爱的","呆若木鸡的","出现BUG的","马路边捡到一分钱","没交给警察叔叔的","只会心疼geigei的","核废水喝多的","开玩笑的","水平不占还跳步的","毁灭世界的","拯救世界的","新东方做饭的","正在钓鱼的","不太正♂常的","正在嫖娼的","撤硕吃饭的","假酒喝多了的","直视了不可名状之神的","持刀行凶的","不怀好意的","上天入地的","发愤图强的","鬼鬼祟祟的","偷偷摸摸的","做“好”事的","蓝翔开挖机的","穿女装的","跳鸡你太美的","开♂车的","撩妹的","手舞足蹈的","非常生气的","懵逼的","正在吃饭的","打游戏的","写作业的","看美女的","看帅哥的","努力学习的","搞事情的","装死的","骂骂咧咧的","疯疯癫癫的","超团子的","湿透了的","涩涩的","发情的","充值天王","喝水的","淹死的","喝城汁的","蹲大牢的","爱吃火锅底料的","红烧的"]
        fish2 = ["鲶鱼","小丑鱼","海胆","鳀鱼","河豚","鲇鱼","水母","虾虎鱼","竹䇲鱼","单角鲀","老虎鱼","青鱼","草鱼","鲢鱼","鳙鱼","方块","清纯鱼","蔡徐鲲","名医鱼","迫击炮鱼","蓝宝石灯鱼","炽天使鱼","鱼糕鱼","巫鱼","加拿大电鳗","伏拉夫","欣然","信息"]
        fish = fish1[random.randint(0,len(fish1)-1)] + fish2[random.randint(0,len(fish2)-1)]
        return f"{称}钓到「{fish}」！获得{add_斯玛特}{后称}"

#商店模板
"""
            elif message.content == 'xx商店':
                await self.api.post_message(channel_id=message.channel_id, content='''xx商店
xxx
xxx
xxx''')
"""

class data():

    async def topcds(database, table, column, user_id, top_n):
        cnx = await aiomysql.connect(user='root', password='马赛克', host='马赛克', db=database)
        cursor = await cnx.cursor()
        query = f"SELECT {column}, id FROM {table} ORDER BY CAST({column} AS UNSIGNED) DESC LIMIT %s"
        params = (top_n,)
        await cursor.execute(query, params)
        results = await cursor.fetchall()
        user_rank = None
        for i, x in enumerate(results):
            if x[1] == user_id:
                user_rank = i
                break
        await cursor.close()
        cnx.close()
        formatted_results = []
        for i, result in enumerate(results):
            village_name = await data.read('村庄', result[1], '村庄名', '0')
            formatted_results.append(f"Top{i+1}：{village_name}：{result[0]}")
        
        if user_rank is not None:
            formatted_results.append(f"你村排行：第{user_rank + 1}名")
        
        return "\n".join(formatted_results)


    async def read(table, some_id, header, default_value=None):
        conn = pymysql.connect(host='马赛克', user='root', passwd='马赛克', port=3306, charset='utf8mb4')
        cur = conn.cursor()
        cur.execute('use fisher;')

        while True:
            cur.execute(f'select {header} from {table} where id=%s', (some_id,))
            res = cur.fetchone()
            if res is None:
                cur.execute(f'insert into {table} (id, {header}) values (%s, %s)', (some_id, default_value))
                conn.commit()
            elif res[0] is None:
                cur.execute(f'update {table} set {header}=%s where id=%s', (default_value, some_id))
                conn.commit()
            else:
                return res[0]

    async def write(table, some_id, header, value):
        conn = pymysql.connect(host='马赛克', user='root', passwd='马赛克', port=3306, charset='utf8')
        cur = conn.cursor()
        cur.execute('use fisher;')
        query = f'select * from {table} where id=%s;'
        cur.execute(query, (some_id,))
        res = cur.fetchall()

        if not res:
            query = f'insert into {table} (id, {header}) values (%s, %s);'
            cur.execute(query, (some_id, value))
            conn.commit()
            #print("数据已成功插入")
        else:
            query = f"update {table} set {header}=%s WHERE id=%s;"
            cur.execute(query, (value, some_id))
            conn.commit()
            #print("数据已成功更新")

        cur.close()
        conn.close()



    async def 属性操作(some_id,header,value,mode):
        some_value = Decimal(await data.read("属性",some_id,header,"100"))
        some_max = Decimal(await data.read("属性",some_id,header+"上限","100"))
        if mode == "sub":
            value = Decimal(value).quantize(Decimal('0.'))
            await data.write("属性",some_id,header,some_value-Decimal(value))
            return f"[{header}]↓{value}"
        elif mode == "add":
            value = Decimal(value)
            if header == "体力":
                value = value*min(1,Decimal(await data.read("属性",some_id,"精力","100"))/Decimal(await data.read("属性",some_id,"精力上限","100")))
                value = value.quantize(Decimal('0.'))
            if some_value <= some_max:
                some_value = (some_value + value).quantize(Decimal('0.'))
                if some_value >= some_max:
                    some_value = some_max
                    msg = f"[{header}]↑→{some_max}(已满)"
                else:
                    msg = f"[{header}]↑{value}"
            else:
                msg = f"[{header}][属性溢出]"
            await data.write("属性",some_id,header,some_value)
            return msg


def run_bot(appid, token):
    intents = botpy.Intents(guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=appid, token=token)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_bot, args=(114514, '马赛克'))
    p2 = multiprocessing.Process(target=run_bot, args=(114514, '马赛克'))
    p3 = multiprocessing.Process(target=run_bot, args=(114514, '马赛克'))
    
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
