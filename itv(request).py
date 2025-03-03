import time
import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
from security import safe_requests

urls = [
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYmVpamluZyI=",  # 北京
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hhbmdoYWki",  # 上海
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0idGlhbmppbiI=",  # 天津
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hvbmdxaW5nIg==",  # 重庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYW5xaW5nIg==",  # 安庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYW5zaGFuIg==",  # 鞍山
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYW55YW5nIg==",  # 安阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYmFpY2hlbmci",  # 白城
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYmFvZGluZyI=",  # 保定
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYmFvamki",  # 宝鸡
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYmluemhvdSI=",  # 滨州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYm96aG91Ig==",  # 亳州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2FuZ3pob3Ui",  # 沧州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hhbmdkZSI=",  # 常德
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hhb3pob3Ui",  # 潮州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hlbmdkdSI=",  # 成都
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hlbnpob3Ui",  # 郴州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hpemhvdSI=",  # 池州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hvbmd6dW8i",  # 崇左
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2h1emhvdSI=",  # 滁州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZGFsaSI=",  # 大理
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZGFueWFuZyI=",  # 丹阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZGFxaW5nIg==",  # 大庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZGF0b25nIg==",  # 大同
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZGF6aG91Ig==",  # 达州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZGV6aG91Ig==",  # 德州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZG9uZ2d1YW4i",  # 东莞
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZG9uZ3lpbmci",  # 东营
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZnV4aW4i",  # 阜新
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZnV5YW5nIg==",  # 阜阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZnV6aG91Ig==",  # 福州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZ2FuemhvdSI=",  # 赣州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZ3Vhbmd6aG91Ig==",  # 广州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZ3VpZ2FuZyI=",  # 贵港
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZ3VpeWFuZyI=",  # 贵阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGFpa291Ig==",  # 海口
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGFuZGFuIg==",  # 邯郸
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGFuZ3pob3Ui",  # 杭州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGViaSI=",  # 鹤壁
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGVmZWki",  # 合肥
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGVuZ3lhbmci",  # 衡阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGV5dWFuIg==",  # 河源
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaGV6ZSI=",  # 菏泽
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaHVhaWh1YSI=",  # 怀化
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaHVhaW5hbiI=",  # 淮南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaHVhbmdnYW5nIg==",  # 黄冈
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaHVhbmdzaGki",  # 黄石
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaHVpemhvdSI=",  # 惠州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaHV6aG91Ig==",  # 湖州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamlhbmdtZW4i",  # 江门
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamlhb3p1byI=",  # 焦作
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamlheGluZyI=",  # 嘉兴
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamlsaW4i",  # 吉林
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluYW4i",  # 济南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluY2hlbmci",  # 晋城
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluZ2RlemhlbiI=",  # 景德镇
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluZ2hvbmci",  # 景洪
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluaHVhIg==",  # 金华
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluaW5nIg==",  # 济宁
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluemhvbmci",  # 晋中
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iamluemhvdSI=",  # 锦州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaml1amlhbmci",  # 九江
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iaml5dWFuIg==",  # 济源
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ia2FpZmVuZyI=",  # 开封
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ia3VubWluZyI=",  # 昆明
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibGFuZ2Zhbmci",  # 廊坊
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibGFuemhvdSI=",  # 兰州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibGlhb2NoZW5nIg==",  # 聊城
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibGlueWki",  # 临沂
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibG91ZGki",  # 娄底
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibHVvaGUi",  # 漯河
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibHVveWFuZyI=",  # 洛阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibWFvbWluZyI=",  # 茂名
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibWVpemhvdSI=",  # 梅州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibXVkYW5qaWFuZyI=",  # 牡丹江
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibmFuY2hhbmci",  # 南昌
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibmFuY2hvbmci",  # 南充
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibmFuamluZyI=",  # 南京
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibmFubmluZyI=",  # 南宁
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibmFueWFuZyI=",  # 南阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibmluZ2JvIg==",  # 宁波
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ibmluZ2RlIg==",  # 宁德
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icGluZ2RpbmdzaGFuIg==",  # 平顶山
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icGluZ3hpYW5nIg==",  # 萍乡
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icHV5YW5nIg==",  # 濮阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icWluZ2RhbyI=",  # 青岛
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icWlvbmdoYWki",  # 琼海
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icXVhbnpob3Ui",  # 泉州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icXV6aG91Ig==",  # 衢州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icml6aGFvIg==",  # 日照
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2FubWVueGlhIg==",  # 三门峡
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2FueWEi",  # 三亚
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGlhbWVuIg==",  # 厦门
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZm9zaGFuIg==",  # 佛山
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hhbmdxaXUi",  # 商丘
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hhb3hpbmci",  # 绍兴
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hhb3lhbmci",  # 邵阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hlbnlhbmci",  # 沈阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hlbnpoZW4i",  # 深圳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hpamlhemh1YW5nIg==",  # 石家庄
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic2hpeWFuIg==",  # 十堰
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic29uZ3l1YW4i",  # 松原
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic3VpbmluZyI=",  # 遂宁
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic3V6aG91Ig==",  # 苏州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0idGFpeXVhbiI=",  # 太原
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0idGFpemhvdSI=",  # 泰州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0idGllbGluZyI=",  # 铁岭
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id2VpZmFuZyI=",  # 潍坊
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id2VpaGFpIg==",  # 威海
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id2VpbmFuIg==",  # 渭南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id2VuemhvdSI=",  # 温州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id3VoYW4i",  # 武汉
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id3VodSI=",  # 芜湖
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id3V4aSI=",  # 无锡
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0id3V6aG91Ig==",  # 梧州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGlhbiI=",  # 西安
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGlhbmd0YW4i",  # 湘潭
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGljaGFuZyI=",  # 西昌
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGlueGlhbmci",  # 新乡
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGlueWFuZyI=",  # 信阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGlueXUi",  # 新余
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ic3VxaWFuIg==",  # 宿迁
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieHVjaGFuZyI=",  # 许昌
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieHV6aG91Ig==",  # 徐州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWFuY2hlbmci",  # 盐城
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWFuZ2ppYW5nIg==",  # 阳江
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWFuZ3pob3Ui",  # 扬州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWFuamki",  # 延吉
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWFudGFpIg==",  # 烟台
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWljaHVuIg==",  # 宜春
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWluZ2tvdSI=",  # 营口
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieWl5YW5nIg==",  # 益阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieW9uZ3pob3Ui",  # 永州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieXVleWFuZyI=",  # 岳阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieXVsaW4i",  # 玉林
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieXVuY2hlbmci",  # 运城
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hhbmdjaHVuIg==",  # 长春
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhhbmdqaWFqaWUi",  # 张家界
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iY2hhbmdzaGEi",  # 长沙
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhhbmd6aG91Ig==",  # 漳州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhhbmppYW5nIg==",  # 湛江
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhhb3Fpbmci",  # 肇庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhhb3Rvbmci",  # 昭通
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhlbmd6aG91Ig==",  # 郑州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhvbmdzaGFuIg==",  # 中山
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhvdWtvdSI=",  # 周口
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemhvdXNoYW4i",  # 舟山
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemh1aGFpIg==",  # 珠海
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemh1bWFkaWFuIg==",  # 驻马店
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemh1emhvdSI=",  # 株洲
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iemlnb25nIg==",  # 自贡
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iZnVxaW5nIg==",  # 福清
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iYmFvdG91Ig==",  # 包头
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieml5YW5nIg==",  # 资阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieGluamki",  # 辛集
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0icWl0YWloZSI=",  # 七台河
    ]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls


def is_url_accessible(url):
    try:
        response = safe_requests.get(url, timeout=1)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


results = []

for url in urls:
    try:
        response = safe_requests.get(url, timeout = 15)
        if response.status_code == 200:
            print(response)
            page_content = response.content.decode('utf-8')

            # 查找所有符合指定格式的网址
            pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
            urls_all = re.findall(pattern, page_content)
            # urls = list(set(urls_all))  # 去重得到唯一的URL列表
            urls = set(urls_all)  # 去重得到唯一的URL列表
            x_urls = []
            for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
                url = url.strip()
                ip_start_index = url.find("//") + 2
                ip_end_index = url.find(":", ip_start_index)
                ip_dot_start = url.find(".") + 1
                ip_dot_second = url.find(".", ip_dot_start) + 1
                ip_dot_three = url.find(".", ip_dot_second) + 1
                base_url = url[:ip_start_index]  # http:// or https://
                ip_address = url[ip_start_index:ip_dot_three]
                port = url[ip_end_index:]
                ip_end = "1"
                modified_ip = f"{ip_address}{ip_end}"
                x_url = f"{base_url}{modified_ip}{port}"
                x_urls.append(x_url)
            urls = set(x_urls)  # 去重得到唯一的URL列表

            valid_urls = []
            #   多线程获取可用url
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = []
                for url in urls:
                    url = url.strip()
                    modified_urls = modify_urls(url)
                    for modified_url in modified_urls:
                        futures.append(executor.submit(is_url_accessible, modified_url))

                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        valid_urls.append(result)

            for url in valid_urls:
                print(url)
            # 遍历网址列表，获取JSON文件并解析
            for url in valid_urls:
                try:
                    # 发送GET请求获取JSON文件，设置超时时间为0.5秒
                    ip_start_index = url.find("//") + 2
                    ip_dot_start = url.find(".") + 1
                    ip_index_second = url.find("/", ip_dot_start)
                    base_url = url[:ip_start_index]  # http:// or https://
                    ip_address = url[ip_start_index:ip_index_second]
                    url_x = f"{base_url}{ip_address}"

                    json_url = f"{url}"
                    response = safe_requests.get(json_url, timeout=1)
                    json_data = response.json()

                    try:
                        # 解析JSON文件，获取name和url字段
                        for item in json_data['data']:
                            if isinstance(item, dict):
                                name = item.get('name')
                                urlx = item.get('url')
                                if 'http' in urlx:
                                    urld = f"{urlx}"
                                else:
                                    urld = f"{url_x}{urlx}"

                                if name and urld:
                                    # 删除特定文字
                                    name = name.replace("cctv", "CCTV")
                                    name = name.replace("中央", "CCTV")
                                    name = name.replace("央视", "CCTV")
                                    name = name.replace("高清", "")
                                    name = name.replace("超高", "")
                                    name = name.replace("HD", "")
                                    name = name.replace("标清", "")
                                    name = name.replace("频道", "")
                                    name = name.replace("-", "")
                                    name = name.replace(" ", "")
                                    name = name.replace("PLUS", "+")
                                    name = name.replace("＋", "+")
                                    name = name.replace("(", "")
                                    name = name.replace(")", "")
                                    name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                                    name = name.replace("CCTV1综合", "CCTV1")
                                    name = name.replace("CCTV2财经", "CCTV2")
                                    name = name.replace("CCTV3综艺", "CCTV3")
                                    name = name.replace("CCTV4国际", "CCTV4")
                                    name = name.replace("CCTV4中文国际", "CCTV4")
                                    name = name.replace("CCTV4欧洲", "CCTV4")
                                    name = name.replace("CCTV5体育", "CCTV5")
                                    name = name.replace("CCTV6电影", "CCTV6")
                                    name = name.replace("CCTV7军事", "CCTV7")
                                    name = name.replace("CCTV7军农", "CCTV7")
                                    name = name.replace("CCTV7农业", "CCTV7")
                                    name = name.replace("CCTV7国防军事", "CCTV7")
                                    name = name.replace("CCTV8电视剧", "CCTV8")
                                    name = name.replace("CCTV9记录", "CCTV9")
                                    name = name.replace("CCTV9纪录", "CCTV9")
                                    name = name.replace("CCTV10科教", "CCTV10")
                                    name = name.replace("CCTV11戏曲", "CCTV11")
                                    name = name.replace("CCTV12社会与法", "CCTV12")
                                    name = name.replace("CCTV13新闻", "CCTV13")
                                    name = name.replace("CCTV新闻", "CCTV13")
                                    name = name.replace("CCTV14少儿", "CCTV14")
                                    name = name.replace("CCTV15音乐", "CCTV15")
                                    name = name.replace("CCTV16奥林匹克", "CCTV16")
                                    name = name.replace("CCTV17农业农村", "CCTV17")
                                    name = name.replace("CCTV17农业", "CCTV17")
                                    name = name.replace("CCTV5+体育赛视", "CCTV5+")
                                    name = name.replace("CCTV5+体育赛事", "CCTV5+")
                                    name = name.replace("CCTV5+体育", "CCTV5+")
                                    urld = urld.replace("udp://@", "/udp/")
                                    urld = urld.replace("udp://", "/udp/")
                                    urld = urld.replace("rtp://@", "/rtp/")
                                    urld = urld.replace("rtp://", "/rtp/")
                                    results.append(f"{name},{urld}")
                    except:
                        continue
                except:
                    continue
    except:
        continue

results = set(results)   # 去重得到唯一的URL列表
results = sorted(results)
with open("itv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        print(result)
