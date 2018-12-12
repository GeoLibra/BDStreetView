import requests
from lxml import etree
import random
import time
import re
import telnetlib
class Proxy:
    def __init__(self):
        self.user_agents=[
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
        ]
        self.url = 'http://www.xicidaili.com/nn/'
    # 将可以使用的代理IP的信息存储到文件
    def write_proxy(sefl,proxies):
        with open("ip_proxy.txt", 'a+') as f:
            f.write('\n'.join(proxies))
    # 解析网页，并得到网页中的代理IP
    def get_proxy(sefl,html):
        speeds=[] # 存放速度；列表,速度最快的放末尾
        # 对获取的页面进行解析
        selector = etree.HTML(html)
        # print(selector.xpath("//title/text()"))
        proxies = []
        # 信息提取
        for each in selector.xpath('//table[@id="ip_list"]/tr')[1:]:
            ip = each.xpath("./td[2]/text()")[0]
            port = each.xpath("./td[3]/text()")[0]


            proxy = ip + ":" + port
            if sefl.test_proxies(proxy):
                s = each.xpath("./td[7]/div/@title")[0]
                speed = float(re.findall(r"\d+\.?\d*", s)[0])
                print(speed)
                print(speeds)
                if len(speeds)==0 or speed<speeds[-1]:
                    speeds.append(speed)
                    proxies.append(proxy)
                else:
                    start=len(speeds)

                    for i in range(0,len(speeds)):
                        if speeds[i]<speed:
                            speeds.insert(i,speed)
                            proxies.insert(i,proxy)
                            break
                    if start==len(speeds):
                        speeds.insert(0, speed)
                        proxies.insert(0, proxy)


        return proxies


    # 验证已得到IP的可用性
    def test_proxies(sefl,proxy):
        ip=proxy.split(':')[0]
        port=proxy.split(':')[1]
        try:
            telnetlib.Telnet(ip,port,timeout=20)
        except:
            return False
        return True
    # def test_proxies(sefl,proxy):
    #     url = ["https://www.qq.com/",
    #            "https://www.zhihu.com",
    #            "https://www.douban.com/",
    #            "https://www.baidu.com/",
    #            "https://blog.csdn.net/",
    #            "https://hao.360.cn/",
    #            "https://www.mi.com/index.html",
    #            "https://www.hao123.com/",
    #            "https://www.163.com/",
    #            "https://www.sohu.com/",
    #            "https://www.fang.com/",
    #            "https://www.youku.com/",
    #            "https://tieba.baidu.com/",
    #            "https://www.jianshu.com",
    #            "https://www.bilibili.com/"
    #            ]
    #     header = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    #     }
    #     response = requests.get(url[random.randint(0, len(url)-1)], headers=header, proxies={"http": proxy}, timeout=500)
    #     if response.status_code == 200:
    #         return True
    #     else:
    #         return False

    def get_html(sefl,url):
        header = {
            "User-Agent":sefl.user_agents[random.randint(0, len(sefl.user_agents)-1)]
        }
        response = requests.get(url,headers=header,timeout=500)
        sefl.write_proxy(sefl.get_proxy(response.text))


if __name__ == "__main__":
    url = 'http://www.xicidaili.com/nn/'
    p=Proxy()
    p.get_html(url)
    # import os
    # ip="219.234.5.128:3128"
    # return1 = os.system('ping -n 1 -w 1 %s' % ip)
    #
    # print(p.test_proxies("219.234.5.128:3128"))
