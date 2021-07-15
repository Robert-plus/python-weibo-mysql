import time
import xpath


def timer():
    while True:
        # 初始化定时时间
        time_now = time.strftime("%S", time.localtime())
        # 当秒数等于以下时
        if (time_now == "50") or (time_now == "20"):
            subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 执行了一次程序"
            print(subject)

            # 执行xpath运行
            xpath.run()

            # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次
            time.sleep(2)


if __name__ == '__main__':
    # 总程序启动
    timer()
