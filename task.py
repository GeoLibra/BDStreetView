import schedule
import time
import proxy
'''
schedule 轻量级的定时任务调度的库
'''

def job():
    url = 'http://www.xicidaili.com/nn/'
    p=proxy.Proxy()
    p.get_html(url)

schedule.every(15).minutes.do(job)
# schedule.every(10).seconds.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1000)