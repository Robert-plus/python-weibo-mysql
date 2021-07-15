# Libraries

import sys
import datetime
import pymysql


def db_connect():
    try:
        db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='echartdemoone'
        )
    except Exception as e:
        print("Can't connect to database")
    return db


def insert_db(rank, affair, view, tag, key_list):
    # 初始化当前时间
    now_time = datetime.datetime.now()
    time1 = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    try:
        # 清空content数据库sql
        sql_delete = "DELETE FROM db_weibo_content"
        # 插入all数据库sql
        sql_table_all = "INSERT INTO db_weibo_all SET note=(%s), num=(%s), real_pos=(%s),onboard_time='" + time1 + "'"
        sql_table_all = "INSERT INTO db_weibo_all(note,num,real_pos,onboard_time,word) VALUES(%s,%s,%s,'" + time1 + "',%s)"
        # 插入content数据库sql
        sql_table_content = "INSERT INTO db_weibo_content(note,num,real_pos,onboard_time,word) VALUES(%s,%s,%s,'" + time1 + "',%s)"
        # 查询all数据库sql,判断此项是否已存在
        sql_select = "SELECT * FROM db_weibo_all WHERE note=(%s)"

        db = db_connect()
        cursor = db.cursor()
        # 整合list准备插入
        values = list(zip(affair, view, rank, key_list))
        # 调试用输出-print(values)

        # 先执行删除操作
        cursor.execute(sql_delete)
        db.commit()
        # 清空content数据库后直接插入
        cursor.executemany(sql_table_content, values)
        db.commit()

        # 循环判断是否已存在
        for i in range(0, len(affair)):
            cursor.execute(sql_select, affair[i])
            data = cursor.fetchall()
            if not data:
                # 调试用输出-print(affair[i])
                print("未找到第" + str(i) + "项,所以执行插入操作")
                cursor.execute(sql_table_all, values[i])
                db.commit()
            else:
                # 调试用输出-print(data)
                print("已经存在了第" + str(i) + "项")

        cursor.close()
        db.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("start")
