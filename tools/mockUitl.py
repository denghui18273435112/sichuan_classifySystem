#-*- coding: utf-8 -*-
#@File    : mockTest.py
#@Time    : 2021/4/9 20:32
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2021/4/9
import threading
import requests
import json
"""
mock技术（测试桩/挡板）使用场景：
    1- 后端某些功能没有实现，测试需要提前介入
    2- 如果项目接口里有很多第三方接口，调用关系比较复杂，耗时比较长
    3- 某些接口没有搞定的情况下，后续又是重点，可以使用mock绕过去！
"""
HOST = "http://127.0.0.1:8888"

def demo1():
    """
    demo1=约定URI 其实就是url
    """
    url = "{}/xintian_sq".format(HOST)
    res = requests.post(url)
    print(res.text)


def demo2():
    """
    demo2=约定请求参数
    """
    url = "{}/sq".format(HOST)
    params = {"key1":"abc","key2":"123"}
    res = requests.post(url,params=params)
    print(res.text)


def demo5():
    """
    demo5=约定请求体参数-form
    """
    url = "{}/sq2".format(HOST)
    data = {"key1":"abc"}
    res = requests.post(url,data=data)
    print(res.text)


def demo6():
    """
    demo6=约定请求体参数-json data=json.dumps(data)
    """
    url = "{}/sq3".format(HOST)
    data = {"key1":"value1","key2":"value2"}
    res = requests.post(url,json=data)
    print(res.text)


def demo13():
    """
    demo6=约定请求体参数-json
    """
    url = "{}/sq4".format(HOST)
    res = requests.post(url)
    print(res.text)


def create_order():
    """
    #1- 提交申诉请求
    """
    url = "{}/api/order/create/".format(HOST)
    json = {
        "user_id":"sq001",
		"goods_id":"1234",
		"num":1,
		"amount":100.8
    }
    resp = requests.post(url,json=json)
    print(resp.json())


"""
#2- 查询申诉请求的结果   使用请求接口的返回id  去查询
查询接口：
    1- 频率   interval
    2- 多少时间超时  timeout
    3- 如果在超时时间内，查到结果就不需要继续查询！
"""
import time
def get_order_result(orderID,interval=3,timeout=20):
    """
    :param orderID: 订单id
    :param interval: 频率    s
    :param timeout: 超时时间  s
    :return:
    """
    url = "{}/api/order/get_result01/".format(HOST)
    payload = {"order_id":orderID}
    #1- 开始时间
    startTime = time.time()#获取当时时间  s单位
    #2- 结束时间
    endTime = startTime + timeout
    #3- 选择循环！
    # while   靠条件结束的----
    #for 知道循环次数 或遍历操作
    cnt = 0#计数变量
    while time.time() < endTime:
        resp = requests.get(url,params=payload)
        cnt += 1
        if resp.text:#有响应数据就结束循环！
            print("第{}次查询，已经有查询结果>>> ".format(cnt),resp.text)
            break
        else:
            print("第{}次查询，没有结果，请稍等...".format(cnt))

        #4- 设置频率
        time.sleep(interval)#间隔多久运行一次
    print("查询完成")

    return resp.text

def demo100():
     #1- 获取id
    id = create_order()
    print(id)
    #2- 查询结果
    res = get_order_result(id)
    print(res)

    """
    t1 = threading.Thread()  创建线程方法
    target  你希望吧哪一个函数作为子线程！
    args  这个函数的实参
    """
    t1 = threading.Thread(target=get_order_result,args=(id,))

    #设置守护线程  主线程退出了，子线程get_order_result 也退出
    t1.setDaemon(True)
    #启动线程
    t1.start()
    """
    扩展知识点：多线程技术---
    并发：
    并行：
        1- io密集型  阻塞
            sleep()  requests库
        2- cpu密集型  计算型---这个多线程不一定省时间！

    预期效果：
        希望在异步查询的等待 3s 的时间，可以去执行其他模块接口！
    """
    for one in range(50):
        time.sleep(1)
        print('{}-----我正在执行其他模块的自动化测试----'.format(one))

def dem22221():
    """
    2-查询订单接口
    :return:
    """
    url = "{}/api/order/get_result/".format(HOST)

    queries = {
					"order_id": "6666"
				}
    resp = requests.get(url,params=queries)
    print(resp.json())


def dem2221():
    """
    1-创建申诉订单接口
    :return:
    """
    url = "{}/api/order/create/".format(HOST)
    json = {
        "user_id": "sq123456",
		"goods_id": "20200815",
		"num":1,
		"amount":200.6
    }
    headers = {
					"Content-Type":"application/json"
				}
    resp = requests.post(url,json=json,headers=headers)
    print(resp.json())

if __name__ == '__main__':
    dem2221()

