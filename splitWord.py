import sys
import os
import re

from weibo import customUtil

StopWordtmp = [' ', u'\u3000', u'\x30fb', u'\u3002', u'\uff0c', u'\uff01', u'\uff1f', u'\uff1a', u'\u201c', u'\u201d',
               u'\u2018', u'\u2019', u'\uff08', u'\uff09', u'\u3010', u'\u3011', u'\uff5b', u'\uff5d', u'-', u'\uff0d',
               u'\uff5e', u'\uff3b', u'\uff3d', u'\u3014', u'\u3015', u'\uff0e', u'\uff20', u'\uffe5', u'\u2022', u'.']

WordDic = {}
StopWord = []
span = 16


def InitStopword():
    for key in StopWordtmp:
        StopWord.append(key)


def InitDic(Dicfile):
    # f = file(Dicfile)20210405替换
    f = open(Dicfile, mode='r', encoding="utf-8")
    for line in f:
        line = line.strip().encode('utf-8').decode('utf-8')
        WordDic[line] = 1
    f.close()
    print(len(WordDic))
    print("Dictionary has built down!")


def WordSeg(affair):
    senList = []
    tmpword = ''
    line = affair
    for i in range(len(line)):
        if line[i] in StopWord:
            senList.append(tmpword)
            senList.append(line[i])
            tmpword = ''
        else:
            tmpword += line[i]
            if i == len(line) - 1:
                senList.append(tmpword)

    # Post
    # 20210623 Robert
    # newsenList = []
    newsenList = ''
    for key in senList:
        if key in StopWord:
            # newsenList.append(key)
            # 无意义执行
            meaningless = 0
        else:
            tmplist = PostSenSeg(key, span)
            # for keyseg in tmplist:
            #     newsenList.append(keyseg)
            # 20210623 Robert
            newsenList = tmplist

    return newsenList


def PostSenSeg(sen, span):
    cur = len(sen)
    pre = cur - span
    if pre < 0:
        pre = 0
    revlist = []
    key_word_list = []
    while 1:
        if cur <= 0:
            break
        s = re.search(
            u"[0|1|2|3|4|5|6|7|8|9|\uff11|\uff12|\uff13|\uff14|\uff15|\uff16|\uff17|\uff18|\uff19|\uff10|\u4e00"
            u"|\u4e8c|\u4e09|\u56db|\u4e94|\u516d|\u4e03|\u516b|\u4e5d|\u96f6|\u5341|\u767e|\u5343|\u4e07|\u4ebf"
            u"|\u5146|\uff2f]+$",
            sen[pre:cur])
        if s:
            if s.group() != '':
                revlist.append(s.group())
            cur = cur - len(s.group())
            pre = cur - span
            if pre < 0:
                pre = 0
        s = re.search(
            u"^[a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y"
            u"|Z|\uff41|\uff42|\uff43|\uff44|\uff45|\uff46|\uff47|\uff48|\uff49|\uff47|\uff4b|\uff4c|\uff4d|\uff4e"
            u"|\uff4f|\uff50|\uff51|\uff52|\uff53|\uff54|\uff55|\uff56|\uff57|\uff58|\uff59|\uff5a|\uff21|\uff22"
            u"|\uff23|\uff24|\uff25|\uff26|\uff27|\uff28|\uff29|\uff2a|\uff2b|\uff2c|\uff2d|\uff2e|\uff2f|\uff30"
            u"|\uff31|\uff32|\uff33|\uff35|\uff36|\uff37|\uff38|\uff39|\uff3a]+",
            sen[pre:cur])
        if s:
            if s.group() != '':
                revlist.append(s.group())
            cur = cur - len(s.group())
            pre = cur - span
            if pre < 0:
                pre = 0

        if (sen[pre:cur] in WordDic) or (cur - 1 == pre):
            if sen[pre:cur] != '':
                revlist.append(sen[pre:cur])
            # Robert修改新增
            if len(sen[pre:cur]) > 1:
                # 20210622应该加的锚点
                # 20210622应该加的锚点
                key_word_list.append(sen[pre:cur])
            cur = pre
            pre = pre - span
            if pre < 0:
                pre = 0
        else:
            pre += 1
    prov_list = ''
    if len(key_word_list):
        prov_name = customUtil.FoundProvByCity(key_word_list[0])
        prov_list = prov_name
    return prov_list
