#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import collections

class ZZWordFreq:


    def __init__(self, N=100000):
        # default: top 100k words
        self.N = N

        self.OUTPUTDSL = "wordfreq.zz.dsl"

        # download http://www.anc.org/SecondRelease/data/ANC-all-count.txt
        # 预处理: 以cp1252格式打开, 转为utf8保存
        #   数据中很多非ASCII字符和怪异标点符号, 过滤掉
        self.ANCFILE = "/e/documents/language/English/frequency/ANC-all-count.txt"

        # download http://www.kilgarriff.co.uk/BNClists/all.num.gz
        # 预处理: 无需
        #   非ASCII字符均以html entity形式编码, 直接过滤掉这类单词
        self.BNCFILE = "/e/documents/language/English/frequency/BNC.all.num.txt"

        # download http://www.pdawiki.com/forum/thread-13667-1-1.html
        # 此词频mdx里含有不同词性分别统计的数据, 只保留最前/小的序号
        # 预处理:
        #   cd /e/goldendict/dicts/mine
        #   readmdict.py -x COCA.Frequency.List.mdx
        #   lynx -force_html -width=1000 --dump COCA.Frequency.List.txt > coca.txt
        #   rm data COCA.Frequency.List.txt -rf
        self.COCAFILE = "/e/goldendict/dicts/mine/coca.txt"

        # 对单词排序时使用的乘子, 应大于最大行号
        self.ORDERMULTIPLIER = 1000000

        self.anc = self.handleANC()
        self.bnc = self.handleBNC()
        self.coca = self.handleCOCA()

        self.metafreqlist = [\
                ('ANC', self.anc), \
                ('BNC', self.bnc), \
                ('COCA', self.coca)]

    # 过滤掉所有含 数字, 特殊符号, 非ASCII字符 的单词, 过滤后:
    #   ANC : 210474 words
    #   BNC : 495404 words
    #   COCA: 362861 words
    def passfilter(self, word):
        matchres = re.match('.*[0-9&*!%:?/]', word) is None
        matchres = matchres and re.match('.*[^\t-~]', word) is None
        return matchres

    # not used
    def getrootdict():
        with open(self.ANCFILE, 'r') as f:
            flines = fANC.readlines()
        rdict = {}
        for line in flines:
            line = line.rstrip().split('\t')
            if len(line) != 4:
                continue
            word = line[0]
            root = line[1]
            rdict[word] = root
        return rdict

    # 将dict对象 {'word':num, ...} 按num进行排序, 返回list对象
    #   num代表词频次数统计时, reverse = True, 按num从大到小排序
    #   num代表已排序的序号时, reverse = False, 按num从小到大排序
    # note: sorted() is unstable
    #   当num代表次数时, 比如很多单词都是10次, 这些单词排序后会乱序
    #   目前对于次数的处理:
    #       num = 次数 * ORDERMULTIPLIER + lineno
    #       即当次数一致时, 按lineno排序, 可解决unstable问题
    def dict2list(self, adict, reverse):
        alist = list(adict.items())
        from operator import itemgetter
        alist = sorted(alist, key = itemgetter(1), reverse = reverse)
        alist = list(item[0] for item in alist)
        return alist

    def handleANC(self):
        with open(self.ANCFILE, 'r') as f:
            flines = f.readlines()

        # 每个单词作为key放入dict中
        lineno = -1
        initdict = {}
        for line in flines:
            lineno += 1
            line = line.rstrip().split('\t')
            if len(line) != 4:
                if not ''.join(line).startswith('Total words : '):
                    print('ANC: unhandled line: ', line)
                continue
            key = line[1]
            value = int(line[3])
            if self.passfilter(key):
                if not key in initdict:
                    initdict[key] = self.ORDERMULTIPLIER*value + lineno
                else:
                    initdict[key] += self.ORDERMULTIPLIER*value

        return self.dict2list(initdict, reverse = True)

    def handleBNC(self):
        with open(self.BNCFILE, 'r') as f:
            flines = f.readlines()

        # 每个单词作为key放入dict中
        lineno = -1
        initdict = {}
        for line in flines:
            lineno += 1
            line = line.rstrip().split(' ')
            if len(line) != 4:
                print('BNC: unhandled line: ', line)
                continue
            key = line[1]
            value = int(line[0])
            if self.passfilter(key):
                if not key in initdict:
                    initdict[key] = self.ORDERMULTIPLIER*value + lineno
                else:
                    initdict[key] += self.ORDERMULTIPLIER*value

        return self.dict2list(initdict, reverse = True)

    def handleCOCA(self):
        with open(self.COCAFILE, 'r') as f:
            flines = f.readlines()
        initdict = {}
        # 处理含统计数字的行
        # 如 '     * 73225 base form of lexical verb' 替换为 73225
        for i in range(len(flines)):
            flines[i] = flines[i].rstrip()
            if flines[i].startswith('     * '):
                flines[i] = re.sub('^     \* ([0-9]+).*', '\g<1>', flines[i])
        # 逆序, 合并数字到单词所在行, 并删除空词头
        initdict = {}
        # for i, line in enumerate(reverse(flines)):
        for i in range(len(flines)-1, 0, -1):
            # 若是以数字开头
            if flines[i].isdigit():
                # 排前面的数字序号更小, 若前面存在数据, 则忽略本条数据
                # 否则可加入dict
                if flines[i-1].startswith('   '):
                    key = flines[i-1].strip()
                    value = int(flines[i])
                    if self.passfilter(key):
                        initdict[key] = value

        return self.dict2list(initdict, reverse = False)

    def printlistinfo(self, desc, alist):
        print('\ndict: ', desc)
        print('len: ', len(alist))
        print('first 10 items: ', alist[:10])
        print('100+ 10 items: ', alist[100:110])
        print('last 10 items: ', alist[-10:])

    def writedsl(self, adict, dslname):
        with open(dslname, 'w') as f:
            f.write('#NAME "ZZ WordFreq"\n')
            f.write('#INDEX_LANGUAGE "English"\n')
            f.write('#CONTENTS_LANGUAGE "English"\n')
            f.write('\n')
            for w in adict:
                f.write(w + '\n')
                freqofaword = adict[w]  # 如 {'BNC': 2, 'ANC': 3, 'COCA': 3}
                for (freqname, freqlist) in self.metafreqlist:
                    if freqname in freqofaword:
                        f.write('\t\\[' + freqname + '\\] ' + \
                                str(freqofaword[freqname]) + '\n')

    def combineall(self):
        for (freqname, freqlist) in self.metafreqlist:
            self.printlistinfo(freqname, freqlist)

        od = collections.OrderedDict()
        for index in range(self.N):
            for (freqname, freqlist) in self.metafreqlist:
                word = freqlist[index]
                if not word in od:
                    od[word] = {}
                od[word][freqname] = index + 1

        print('\nN = ', str(self.N))
        print('Total words in final dict: ' + str(len(od)))
        print('Ex: "of" ', od['of'])

        self.writedsl(od, self.OUTPUTDSL)
        print("\ndsl dict created.")

if __name__ == '__main__':
    zz = ZZWordFreq(N=100000)
    zz.combineall()
