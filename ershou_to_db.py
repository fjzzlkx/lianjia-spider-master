#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# read data from csv, write to mysql

import os
import pymysql

from lib.utility.path import DATA_PATH
from lib.city.city import *
from lib.utility.date import *
from lib.utility.version import PYTHON_3
import datetime
import time

pymysql.install_as_MySQLdb()


def create_prompt_text():
    city_info = list()
    num = 0
    for en_name, ch_name in cities.items():
        num += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if num % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city data do you want to save ?\n' + ''.join(city_info)


if __name__ == '__main__':
    # 设置目标数据库
    # mysql or mongodb or excel
    # database = "mysql"
    # database = "mongodb"
    database = "excel"
    db = None
    collection = None
    workbook = None

    if database == "mysql":
        import records

        db = records.Database('mysql://root:E#xsw2ZA@100.69.216.50/lianjia?charset=utf8', encoding='utf-8')
        # db = records.Database('mysql://root:E#xsw2ZA@localhost/lianjia?charset=utf8', encoding='utf-8')
    elif database == "mongodb":
        from pymongo import MongoClient

        conn = MongoClient('localhost', 27017)
        db = conn.lianjia  # 连接lianjia数据库，没有则自动创建
        collection = db.ershou  # 使用ershou集合，没有则自动创建
    elif database == "excel":
        import xlsxwriter

        workbook = xlsxwriter.Workbook('ershou.xlsx')
        worksheet = workbook.add_worksheet()

    # 让用户选择爬取哪个城市的二手房小区价格数据
    prompt = create_prompt_text()
    import sys

    if sys.version_info < (3, 0):  # 如果小于Python3
        city = raw_input(prompt)
    else:
        city = input(prompt)

    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    modify_date = get_date_string()
    # 获得 csv 文件路径
    # modify_date = "20180331"   # 指定采集数据的日期
    # city = "sh"         # 指定采集数据的城市
    city_ch = get_chinese_city(city)
    csv_dir = "{0}/ershou/{1}/{2}".format(DATA_PATH, city, modify_date)

    files = list()
    if not os.path.exists(csv_dir):
        print("{0} does not exist.".format(csv_dir))
        print("Please run 'python ershou.py' firstly.")
        print("Bye.")
        exit(0)
    else:
        print('OK, start to process ' + get_chinese_city(city))
    for csv in os.listdir(csv_dir):
        data_csv = csv_dir + "/" + csv
        # print(data_csv)
        files.append(data_csv)

    # 清理数据
    count = 0
    row = 0
    col = 0
    for csv in files:
        with open(csv, 'r') as f:
            for line in f:
                count += 1

                text = line.strip()
                try:
                    # 如果小区名里面没有逗号，那么总共是6项
                    if text.count(',') == 17:
                        modify_date, district, area, xiaoqu, huxing, mianji, chaoxiang, zhuangxiu, dianti, describes, totalprice, \
                        unitprice, loucheng, height, niandai, guanzhu, daikan, fabushijian = text.split(',')
                    else :
                        print("----------------h")
                        # print(text.count(','))
                        continue
                except Exception as e:
                    print(text)
                    print(e.message)
                    continue
                # sale = sale.replace(r'套在售二手房', '')
                # price = price.replace(r'暂无', '0')
                # price = price.replace(r'元/m2', '')
                # price = int(price)
                # sale = int(sale)

                try :
                    # area
                    # xiaoqu
                    # huxing
                    mianji = mianji.replace(r'平米', '')
                    mianji = float(mianji)
                    # chaoxiang
                    # zhuangxiu
                    # dianti
                    # describes
                    totalprice = totalprice.replace(r'万', '').split(".")[0]
                    totalprice = int(totalprice) * 10000
                    unitprice = unitprice.replace(r'单价', '')
                    unitprice = unitprice.replace(r'元/平米', '')
                    unitprice = int(unitprice)
                    # loucheng
                    height = height.replace(r'共', '')
                    if database == 'mysql':
                        niandai = niandai + '-01-01 00:00:00'
                        niandai = time.strptime(niandai, '%Y-%m-%d %H:%M:%S')

                    guanzhu = guanzhu.replace(r'人关注', '')
                    daikan = daikan.replace(r'共', '')
                    daikan = daikan.replace(r'次带看', '')
                    fabushijian = fabushijian.replace(r'发布', '')
                except (ValueError):
                    print("-------------")
                    continue


                # print("{0} {1} {2} {3} {4} {5}".format(modify_date, district, area, ershou, price, sale))
                print( "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14} {15} {16}".format(modify_date, district,
                                                                                                        area, xiaoqu,
                                                                                                        huxing, mianji,
                                                                                                        chaoxiang,
                                                                                                        zhuangxiu,
                                                                                                        dianti, describes,
                                                                                                        totalprice,
                                                                                                        unitprice,
                                                                                                        loucheng,
                                                                                                        height, niandai,
                                                                                                        guanzhu, daikan,
                                                                                                        fabushijian))
                # 写入mysql数据库
                if database == "mysql":
                    db.query(
                        'INSERT INTO ershou (city, modify_date, district, area, xiaoqu, huxing, mianji, chaoxiang, zhuangxiu, dianti, describes, totalprice, unitprice, loucheng, height, niandai, guanzhu, daikan, fabushijian) ' 
                        'VALUES(:city, :modify_date, :district, :area, :xiaoqu, :huxing, :mianji, :chaoxiang, :zhuangxiu, :dianti, :describes, :totalprice, :unitprice, :loucheng, :height, :niandai, :guanzhu, :daikan, :fabushijian)',
                        city=city_ch, modify_date=modify_date, district=district, area=area, xiaoqu=xiaoqu, huxing=huxing,mianji=mianji, chaoxiang=chaoxiang, zhuangxiu=zhuangxiu, dianti=dianti, describes=describes,
                        totalprice=totalprice, unitprice=unitprice, loucheng=loucheng, height=height, niandai=niandai,guanzhu=guanzhu, daikan=daikan, fabushijian=fabushijian)
                # 写入mongodb数据库
                elif database == "mongodb":
                    data = dict(city=city_ch, modify_date=modify_date, district=district, area=area, ershou=ershou, price=price,
                                sale=sale)
                    collection.insert(data)
                elif database == "excel":
                    if not PYTHON_3:
                        worksheet.write_string(row, col, unicode(city_ch, 'utf-8'))
                        worksheet.write_string(row, col + 1, modify_date)
                        worksheet.write_string(row, col + 2, unicode(district, 'utf-8'))
                        worksheet.write_string(row, col + 3, unicode(area, 'utf-8'))
                        worksheet.write_string(row, col + 4, unicode(ershou, 'utf-8'))
                        worksheet.write_number(row, col + 5, price)
                        worksheet.write_number(row, col + 6, sale)
                    else:
                        try:
                            worksheet.write_string(row, col, modify_date)
                            worksheet.write_string(row, col + 1, district)
                            worksheet.write_string(row, col + 2, area)
                            worksheet.write_string(row, col + 3, xiaoqu)
                            worksheet.write_string(row, col + 4, huxing)
                            worksheet.write_number(row, col + 5, mianji)
                            worksheet.write_string(row, col + 6, chaoxiang)
                            worksheet.write_string(row, col + 7, zhuangxiu)
                            worksheet.write_string(row, col + 8, dianti)
                            worksheet.write_string(row, col + 9, describes)
                            worksheet.write_number(row, col + 10, totalprice)
                            worksheet.write_number(row, col + 11, unitprice)
                            worksheet.write_string(row, col + 12, loucheng)
                            worksheet.write_string(row, col + 13, height)
                            worksheet.write_string(row, col + 14, niandai)
                            worksheet.write_string(row, col + 15, guanzhu)
                            worksheet.write_string(row, col + 16, daikan)
                            worksheet.write_string(row, col + 17, fabushijian)
                        except (ValueError):
                            print(e.message)
                            continue
                    row += 1
    if database == "excel":
        workbook.close()
    print("Total write {0} items to database.".format(count))
