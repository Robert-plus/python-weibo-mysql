import requests
from lxml import etree
import mysql
import splitWord


def run():
    # 定义爬取的url
    url = "https://s.weibo.com/top/summary"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.103 Safari/537.36'}
    html = etree.HTML(requests.get(url, headers=header).text)
    # 获取置顶热搜
    rank = html.xpath('//td[@class="td-01 ranktop"]/text()')
    # 获取热搜内容
    affair = html.xpath('//td[@class="td-02"]/a/text()')
    # 获取点击数值
    view = html.xpath('//td[@class="td-02"]/span/text()')
    # 获取热搜类别标签
    tag = html.xpath('//td[@class="td-03"]')
    # 单独拿出置顶标签
    top_tag = tag[0].xpath("string(.)")
    # 单独拿出置顶内容
    top = affair[0]
    affair = affair[1:]

    # 置顶输出
    # 调试用输出-print('{0:<10}\t{1:<40}\t{2:>20}'.format("top", top, top_tag))
    # 循环输出
    # 调试用输出-for i in range(0, len(affair)):
    # 调试用输出-print("{0:<10}\t{1:{3}<30}\t{2:{3}>20}".format(rank[i], affair[i], view[i], chr(12288)))

    # 初始化定义删次指数
    del_index = 0
    for a in range(0, len(tag)):
        if tag[a].xpath("string(.)") == "荐":
            print(a)
            print("项为荐")
            # 删掉广告项
            # tag数比affair数多1，假设3为荐时，实际是要删affair[2]
            del rank[a - 1 - del_index]
            del view[a - 1 - del_index]
            del affair[a - 1 - del_index]
            # 删掉一次就改变了list的长度及顺序
            del_index += 1

    # 初始化关键词数组
    key_list = []
    # 将StringList转换为NumList
    view = list(map(int, view))

    # Dicfile = "mySelfDict.txt"
    Dicfile = "cityDict.txt"
    splitWord.InitDic(Dicfile)
    splitWord.InitStopword()
    for af in range(0, len(affair)):
        result = splitWord.WordSeg(affair[af])
        print(affair[af])
        key_list.append(result)
        print(result)

    # print(key_list)
    # 调用mysql存入数据库
    mysql.insert_db(rank, affair, view, tag, key_list)


if __name__ == '__main__':
    # 执行一次
    run()
