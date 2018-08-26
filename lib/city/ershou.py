#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 二手房信息的数据结构

import sys
from lib.utility.version import PYTHON_3
if not PYTHON_3:   # 如果小于Python3
    reload(sys)
    sys.setdefaultencoding("utf-8")


class ErShou(object):
    # def __init__(self, district, area, name, price, desc):
    #     self.district = district
    #     self.area = area
    #     self.price = price
    #     self.name = name
    #     self.desc = desc

    def __init__(self, district, area, xiaoqu, huxing, mianji, chaoxiang, zhuangxiu, dianti, desc,
                 totalprice, unitprice, loucheng, height, niandai, guanzhu, daikan, fabushijian):
        self.district = district
        self.area = area
        self.xiaoqu = xiaoqu
        self.huxing = huxing
        self.mianji = mianji
        self.chaoxiang = chaoxiang
        self.zhuangxiu = zhuangxiu
        self.dianti = dianti
        self.desc = desc
        self.totalprice = totalprice
        self.unitprice = unitprice
        self.loucheng = loucheng
        self.height = height
        self.niandai = niandai
        self.guanzhu = guanzhu
        self.daikan = daikan
        self.fabushijian = fabushijian
    # def text(self):
    #     return self.district + "," + \
    #             self.area + "," + \
    #             self.name + "," + \
    #             self.price + "," + \
    #             self.desc

    def text(self):
        return self.district + "," + \
               self.area + "," + \
               self.xiaoqu + "," + \
               self.huxing + "," + \
               self.mianji + "," + \
               self.chaoxiang + "," + \
               self.zhuangxiu + "," + \
               self.dianti + "," + \
               self.desc + "," + \
               self.totalprice + "," + \
               self.unitprice + "," + \
               self.loucheng + "," + \
               self.height + "," + \
               self.niandai + "," + \
               self.guanzhu + "," + \
               self.daikan + "," + \
               self.fabushijian
