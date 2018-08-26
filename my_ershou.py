#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 获得指定城市的二手房数据
#import BeautifulSoup as BeautifulSoup

import threadpool
import threading
from lib.utility.date import *
from lib.city.area import *
from lib.utility.path import *
from lib.url.xiaoqu import *
from lib.city.city import *
from lib.city.ershou import *
from lib.utility.version import PYTHON_3
from lib.const.spider import thread_pool_size
from bs4 import BeautifulSoup
# import re


def collect_area_ershou(city_name, area_name, fmt="csv"):
    """
    对于每个板块,获得这个板块下所有二手房的信息
    并且将这些信息写入文件保存
    :param city_name: 城市
    :param area_name: 板块
    :param fmt: 保存文件格式
    :return: None
    """
    global total_num, today_path

    csv_file = today_path + "/{0}.csv".format(area_name)
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        ershous = get_area_ershou_info(city_name, area_name)
        # 锁定
        if mutex.acquire(1):
            total_num += len(ershous)
            # 释放
            mutex.release()
        if fmt == "csv":
            for ershou in ershous:
                # print(date_string + "," + xiaoqu.text())
                f.write(date_string + "," + ershou.text()+"\n")
    print("Finish crawl area: " + area_name + ", save data to : " + csv_file)


def get_area_ershou_info(city_name, area_name):
    """
    通过爬取页面获得城市指定版块的二手房信息
    :param city_name: 城市
    :param area_name: 版块
    :return: 二手房数据列表
    """
    district_name = area_dict.get(area_name, "")
    chinese_district = get_chinese_district(district_name)
    chinese_area = chinese_area_dict.get(area_name, "")

    ershou_list = list()
    page = 'http://{0}.lianjia.com/ershoufang/{1}/'.format(city_name, area_name)
    print(page)
    headers = create_headers()
    response = requests.get(page, timeout=10, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    try:
        page_box = soup.find_all('div', class_='page-box')[0]
        matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
        total_page = int(matches.group(1))
    except Exception as e:
        print("\tWarning: only find one page for {0}".format(area_name))
        print("\t" + e.message)
        total_page = 1


    # 从第一页开始,一直遍历到最后一页
    for num in range(1, total_page + 1):
        page = 'http://{0}.lianjia.com/ershoufang/{1}/pg{2}'.format(city_name, area_name, num)
        print(page)
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_elements = soup.find_all('li', class_="clear")
        for house_elem in house_elements:

            # 获取div数据
            totalPrice = house_elem.find('div', class_="totalPrice").text.replace("\n", "").strip()
            unitPrice = house_elem.find('div', class_="unitPrice").text.replace("\n", "").strip()
            title = house_elem.find('div', class_='title').text.replace("\n", "").strip()
            houseInfo = house_elem.find('div', class_="houseInfo").text.replace("\n", "").strip()
            flood = house_elem.find('div', class_="flood").text.replace("\n", "").strip()
            followInfo = house_elem.find('div', class_="followInfo").text.replace("\n", "").strip()

            # 数据处理
            # 板块
            area = flood.split(" -  ")[-1]
            house_infos = houseInfo.split(" | ")
            xiaoqu = house_infos[0]
            huxing = house_infos[1]
            mianji = house_infos[2]
            chaoxiang = house_infos[3]
            try :
                zhuangxiu = house_infos[4]
            except (IndexError) :
                continue
            try :
                dianti = house_infos[5]
            except (IndexError) :
                dianti = '未知'
            desc = title
            totalprice = totalPrice
            unitprice = unitPrice
            loucheng = flood[0:3]
            height = flood[4:-1].split(")")[0]
            try :
                niandai = flood.split(")")[1][0:4]
                if niandai[0] != '1' and niandai[0] != '2':
                    continue
            except (IndexError) :
                print(niandai)
                continue
            follow_infos = followInfo.split(" / ")
            guanzhu = follow_infos[0]
            daikan = follow_infos[1]
            fabushijian = follow_infos[2]

            # print(area)
            # print(xiaoqu)
            # print(huxing)
            # print(mianji)
            # print(chaoxiang)
            # print(zhuangxiu)
            # print(dianti)
            # print(desc)
            # print(totalprice)
            # print(unitprice)
            # print(loucheng)
            # print(height)
            # print(niandai)
            # print(guanzhu)
            # print(daikan)
            # print(fabushijian)

            # 作为对象保存
            ershou = ErShou(chinese_district, area, xiaoqu, huxing, mianji, chaoxiang, zhuangxiu, dianti, desc,
                            totalprice, unitprice, loucheng, height, niandai, guanzhu, daikan, fabushijian)
            ershou_list.append(ershou)
    return ershou_list


# -------------------------------
# main函数从这里开始
# -------------------------------
if __name__ == "__main__":

    # i = get_area_ershou_info('sz', 'baishilong')
    #
    # if i != 100:
    #     exit()
    # 让用户选择爬取哪个城市的二手房小区价格数据
    prompt = create_prompt_text()
    # 判断Python版本
    if not PYTHON_3:  # 如果小于Python3
        # city = raw_input(prompt)
        city = 'sz'
    else:
        city = input(prompt)
    print('OK, start to crawl ' + get_chinese_city(city))

    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date_string = get_date_string()
    print('Today date is: %s' % date_string)
    today_path = create_date_path("ershou", city, date_string)

    mutex = threading.Lock()    # 创建锁
    total_num = 0               # 总的小区个数，用于统计
    t1 = time.time()            # 开始计时

    # 获得城市有多少区列表, district: 区县
    districts = get_districts(city)
    print('City: {0}'.format(city))
    print('Districts: {0}'.format(districts))

    # 获得每个区的板块, area: 板块
    areas = list()
    for district in districts:
        areas_of_district = get_areas(city, district)
        print('{0}: Area list:  {1}'.format(district, areas_of_district))
        # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        areas.extend(areas_of_district)
        # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        for area in areas_of_district:
            area_dict[area] = district
    print("Area:", areas)
    print("District and areas:", area_dict)

    # 准备线程池用到的参数
    nones = [None for i in range(len(areas))]
    city_list = [city for i in range(len(areas))]
    args = zip(zip(city_list, areas), nones)
    # areas = areas[0: 1]   # For debugging

    # 针对每个板块写一个文件,启动一个线程来操作
    pool_size = thread_pool_size
    pool = threadpool.ThreadPool(pool_size)
    my_requests = threadpool.makeRequests(collect_area_ershou, args)
    [pool.putRequest(req) for req in my_requests]
    pool.wait()
    pool.dismissWorkers(pool_size, do_join=True)        # 完成后退出

    # 计时结束，统计结果
    t2 = time.time()
    print("Total crawl {0} areas.".format(len(areas)))
    print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, total_num))
