import requests
import time
import datetime
import json
import proxy as pp
from contextlib import closing
class BaiduAPI():

    def search_photo(self, name, token, proxy,longitude, latitude, head, imgW, imgH):
        params = {
            "ak": token,
            "coordtype": "wgs84ll",  # wgs84ll bd09ll gcj02
            "location": "{0},{1}".format(longitude, latitude),
            "fov": 90,  #设置为360即为全景图
            # "pitch":0, # 垂直视角
            "heading": head,
            "width": imgW,
            "height": imgH
        }
        # Download pictures
        with closing(requests.get("http://api.map.baidu.com/panorama/v2", params, stream=True, proxies={"http": proxy},timeout=500)) as r:

            try:
                result = r.content.decode('utf-8')
                result = json.loads(result)
                if result['status'] == '302':
                    return 0
                elif result['status'] == '402':
                    s = name + ',' + longitude + ',' + latitude
                    open('un.txt', 'a').write(s + '\n')
                    return 1
                else:
                    # 获取出问题的写入日志
                    open('log.txt',
                         'a').write(result + ";" + token + ';' + name + '\n')
                    return 0
            except Exception as e:

                # open("./photos/" + name + "_{0}.png".format(head),
                #      'wb').write(r.content)
                with open("./photos/" + name + "_{0}.png".format(head),'rb') as f:
                    for chunk in r.iter_content(128):
                        f.write(chunk)
                    return 1

    def tokens(self):
        f = open("token.txt", "r")
        return [line.strip() for line in f.readlines()]

    def validtoken(self):
        tokens = baidu.tokens()
        data = []
        for token in tokens:
            token = token.strip()
            url = 'http://api.map.baidu.com/panorama/v2?ak=' + token + '&width=512&height=256&location=116.313393,40.04778&fov=180  '
            r = requests.get(url)
            try:
                result = r.content.decode('utf-8')
                if "APP" in result:  # 失效的
                    print(token)
                    print(result)
                else:
                    data.append(token)
            except Exception as e:
                print(e)
                print(r.content)
                open("./photos/" + token + ".png", 'wb').write(r.content)
                data.append(token)
        f = open("valid.txt", 'w')
        f.write('\n'.join(data))
        f.close()
    def getProxy(self):
        f = open('ip_proxy.txt', 'r')
        proxy = [i.strip() for i in f.readlines()]
        f.close()
        return proxy

if __name__ == '__main__':
    # imgW=1024 # 0-1024
    # imgH=512 # 10-512
    imgW = 600  # 0-1024
    imgH = 400  # 10-512
    baidu = BaiduAPI()
    tokens = baidu.tokens()
    today = datetime.date.today()
    first = tokens[0].strip()
    # baidu.validtoken()
    f = open('count.txt', 'r')
    count = int(f.readlines()[0])
    proxy_time=time.time() # 代理使用时间
    proxys=baidu.getProxy()
    proxy=proxys.pop()
    p = pp.Proxy()
    with open('sz_sample.csv', 'r', encoding='utf-8') as data:
        lines = data.readlines()[count-1:]
        for line in lines:
            line = line.strip()
            name = line.split(',')[0]
            open("count.txt", 'w+').write(name)
            longitude = line.split(',')[1].strip()
            latitude = line.split(',')[2].strip()
            if time.time()-proxy_time>8*60:
                # 超过8分钟切换一次代理
                proxy_time=time.time()
                if len(proxys)==0:
                    proxys=baidu.getProxy()
                proxy=proxys.pop()
            headings = [0, 90, 180, 270]

            for head in headings:
                while p.test_proxies(proxy)==False:
                    if len(proxys) == 0:
                        proxys = baidu.getProxy()
                    proxy = proxys.pop()

                result = baidu.search_photo(name, tokens[0], proxy,longitude,
                                            latitude, head, imgW, imgH)
                # print(head, line)
                while result == 0:
                    # time.sleep(10)
                    # 超过限制
                    tokens.append(tokens[0])  # 将第一个添加到末尾
                    tokens.pop(0)  # 将第一个元素删除
                    print(tokens)
                    if tokens[0] == first:
                        now = datetime.date.today()
                        if now != today:  # 超过一天,可以继续使用
                            while p.test_proxies(proxy) == False:
                                if len(proxys) == 0:
                                    proxys = baidu.getProxy()
                                proxy = proxys.pop()
                            result = baidu.search_photo(
                                name, tokens[0], longitude,proxy, latitude, head,
                                imgW, imgH)
                        else:  # 小于24小时
                            print("开始休息,等明天:")
                            print(
                                time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime()))
                            # 今天日期
                            today = datetime.date.today()
                            # 明天时间
                            tomorrow = today + datetime.timedelta(days=1)
                            # 今天结束时间戳
                            today_end_time = int(
                                time.mktime(
                                    time.strptime(str(tomorrow),
                                                  '%Y-%m-%d'))) - 1
                            rest = today_end_time - time.time() + 60
                            m, s = divmod(rest, 60)
                            h, m = divmod(m, 60)
                            print("剩余时间:%02d:%02d:%02d" % (h, m, s))
                            time.sleep(rest)  # 开始休息
                            print("天亮了,继续工作")
                            print(
                                time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime()))
                            today = datetime.date.today()  # 重新计时
                            while p.test_proxies(proxy) == False:
                                if len(proxys) == 0:
                                    proxys = baidu.getProxy()
                                proxy = proxys.pop()
                            result = baidu.search_photo(
                                name, tokens[0],proxy, longitude, latitude, head,
                                imgW, imgH)
                    else:
                        while p.test_proxies(proxy) == False:
                            if len(proxys) == 0:
                                proxys = baidu.getProxy()
                            proxy = proxys.pop()
                        result = baidu.search_photo(name, tokens[0], proxy,longitude,
                                                    latitude, head, imgW, imgH)

