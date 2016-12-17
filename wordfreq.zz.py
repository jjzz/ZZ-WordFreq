#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import collections

class wordfreq:
    def __init__(self):
        # http://www.anc.org/SecondRelease/data/ANC-all-count.txt
        # 预处理: 以cp1252格式打开, 转为utf8保存
        #   数据中很多非ASCII字符和怪异标点符号, 过滤掉
        self.ANCFILE = "/data/doc/language/english/frequency/ANC-all-count.txt"

        # http://www.kilgarriff.co.uk/BNClists/all.num.gz
        # 预处理: 无需
        #   非ASCII字符均以html entity形式编码, 直接过滤掉这类单词
        self.BNCAKFILE = "/data/doc/language/english/frequency/bnc.kilgarriff/BNC.all.num.txt"

        # http://www.pdawiki.com/forum/thread-13667-1-1.html
        # 此词频mdx里含有不同词性分别统计的数据, 只保留最前/小的序号
        # 预处理:
        #   readmdict.py -x COCA.Frequency.List.mdx
        #   lynx -force_html -width=1000 --dump COCA.Frequency.List.txt > coca.txt
        #   rm data COCA.Frequency.List.txt -rf
        self.COCAFILE = "/data/doc/language/english/frequency/coca.mdict/coca.txt"

        # http://www.victoria.ac.nz/lals/about/staff/publications/paul-nation
        #   download "Range program with British National Corpus list"
        #   有两个版本: 14000版 和 25000版, 目前取14000版, 含14组14000个families
        #   14000版的 basewrd15.txt 是专有词汇, 许多较生僻, 忽略
        self.BNCPNROOTDIR = "/data/doc/language/english/frequency/bnc.paulnation/BNC-14000-and-programs-and-instructions/"
        self.BNCPNROOTDIRFILES = 14

        self.bncpn = self.handleBNCPN()
        self.bncak = self.handleBNCAK()
        self.anc = self.handleANC()
        self.coca = self.handleCOCA()

        self.metafreqlist = [
                ("BNC.PN",  self.bncpn, 1000000),
                ("BNC.AK",  self.bncak,   60000),
                ("ANC",     self.anc,     60000),
                ("COCA",    self.coca,    60000),
                ]

    def isgoodword(self, word):
        return re.match('.*[^a-zA-Z \-]', word) is None

    # not used
    def getrootdict():
        with open(self.ANCFILE, 'r') as f:
            flines = fANC.readlines()
        rdict = {}
        for line in flines:
            line = line.strip().split('\t')
            if len(line) != 4:
                continue
            word = line[0]
            root = line[1]
            rdict[word] = root
        return rdict

    def handleANC(self):
        '''
            ANC频率表:
                the     the     DT      1204816
                of      of      IN      606545
                and     and     CC      595372
            说明:
                最后一行为汇总
                同一单词可能因不同词性(第三列)而出现在多行中
            返回字典:
                {"the":[1, None], "of":[2, None], ...}
        '''
        print("initializing ANC dict ...")
        with open(self.ANCFILE, 'r') as f:
            flines = f.readlines()
        seq_no = 0
        initdict = {}
        for line in flines:
            line = line.strip().split('\t')
            if len(line) != 4:
                if not ''.join(line).startswith('Total words : '):
                    print('ANC: wrong line: ', line)
                continue
            key = line[1]
            value = int(line[3])
            if self.isgoodword(key) and not key in initdict:
                seq_no += 1
                initdict[key] = [seq_no, None]
        return sorted(initdict.items(), key=lambda x:x[1][0])

    def handleBNCAK(self):
        '''
            BNC.AK 频率表:
                100106029 !!WHOLE_CORPUS !!ANY 4124
                6187267 the at0 4120
                2941444 of prf 4108
                2682863 and cjc 4120
            说明:
                首行是汇总
                同一单词可能因不同词性(第三列)而出现在多行中
            返回字典:
                {"the":[1, None], "of":[2, None], ...}
        '''
        print("initializing BNC.AK dict ...")
        with open(self.BNCAKFILE, 'r') as f:
            flines = f.readlines()
        seq_no = 0
        initdict = {}
        for line in flines:
            line = line.strip().split(' ')
            if len(line) != 4:
                print('BNCAK: unhandled line: ', line)
                continue
            key = line[1]
            if self.isgoodword(key) and not key in initdict:
                seq_no += 1
                initdict[key] = [seq_no, None]
        return sorted(initdict.items(), key=lambda x:x[1][0])

    def handleBNCPN(self):
        '''
            BNC.PN频率表, 词根部分:
                ALSO 0
                ALTHOUGH 0
                ALWAYS 0
                    ALLUS 0
                AMAZE 0
                    AMAZED 0
                    AMAZEMENT 0
                    AMAZES 0
            说明:
                所有单词按 word family 组织, 每个family 有一个 root
                每个文件1000个root, 文件内按字母顺序排序, 文件间则按词频排序
                每个root后续的缩进行代表word family 内其他单词
                有许多变体如 hôtel 是作为对应词根 hotel 的 family member
                isgoodword 会过滤掉这些非ASCII的单词
            返回字典:
                {"the":[1, None], "of":[2, None], ...}
        '''
        print("initializing BNC-paul-nation dict ...")
        curroot = None
        initdict = {}
        seq_no = 0
        for i in range(self.BNCPNROOTDIRFILES):
            idbatch = (i + 1) * 1000
            filename = self.BNCPNROOTDIR + "basewrd{}.txt".format(i+1)
            print("handling ", filename)
            with open(filename, 'r') as f:
                flines = f.readlines()
            for line in flines:
                isroot = not line.startswith('\t')
                line = line.strip().lower()
                if not line:
                    continue
                line = line.split()[0]
                if not self.isgoodword(line):
                    print("  ignore: ", line)
                    continue
                elif isroot:
                    curroot = line
                    initdict[curroot] = [idbatch, None]
                elif curroot:
                    initdict[line] = [idbatch, curroot]
                    updatestr = initdict[curroot][1]
                    if updatestr:
                        updatestr += ", " + line
                    else:
                        updatestr = line
                    initdict[curroot] = [idbatch, updatestr]
                else:
                    print("  wrong line: ", line)
        return sorted(initdict.items(), key=lambda x:x[1][0])

    def handleCOCA(self):
        '''
            COCA频率表:
                'a
                    * 496637 have, infinitive
                ...
                the
                    * 1 article (e.g. the, no)
                    * 5375 general preposition
            说明:
                每个单词出现一次
                紧接着缩进多行, 列出词性及相应词频排名, 取第一个即可
            返回字典:
                {"the":[1, None], "and":[2, None], ...}
        '''
        print("initializing COCA dict ...")
        with open(self.COCAFILE, 'r') as f:
            flines = f.readlines()
        initdict = {}
        key = None
        for line in flines:
            # 将 '* 73225 base ....' 替换为其中的数字 73225
            line = re.sub('^(\* [0-9]+).*', '\g<1>', line.strip())
            if line == '':
              continue
            # 取紧跟下一行的数字(value)作为单词(key)的排名
            if not re.match('^\* [0-9]', line):
                if self.isgoodword(line):
                    key = line
                    initdict[key] = [0, None]
                else:
                    key = None
            elif key:
                initdict[key][0] += int(line[2:])
                key = None
        tmplist = sorted(initdict.items(), key=lambda x:x[1][0])
        # 修正排序中的空洞, 比如the 排no.1和1000, 则1000处为空洞
        for i in range(len(tmplist)):
            tmplist[i][1][0] = i + 1
        return tmplist

    def printlistinfo(self):
        for (name, data, limit) in self.metafreqlist:
            limit = min(limit, len(data))
            print("{} - {}/{}".format(name, limit, len(data)))
            print('   ex: first 3 items: ', data[:3])
            print('        100+ 3 items: ', data[100:103])
            print('        last 3 items: ', data[limit-3:limit])

    def writedsl(self, od, dslname):
        print("writing dsl file ...")
        with open(dslname, 'w') as f:
            f.write('#NAME "ZZ WordFreq"\n')
            f.write('#INDEX_LANGUAGE "English"\n')
            f.write('#CONTENTS_LANGUAGE "English"\n')
            f.write('\n')
            for word in od:
                f.write(word + '\n')
                for dictname, (rank, desc) in od[word]:
                    # rank, desc = od[word][dictname]
                    if not desc:
                        desc = ""
                    f.write('\t\\[{}\\] {} {}\n'.format(dictname, rank, desc))

    def combineall(self):
        '''
            合并后的字典格式, 值为另一个字典
            "the": {
                'BAK.PN': (1, 'addi,info,here'),
                'BNC.AK': (1, None),
                'ANC': (1, None)
                }
        '''
        print("combining all dicts ...")
        od = collections.OrderedDict()
        for (name, data, limit) in self.metafreqlist:
            for i in range(min(limit, len(data))):
                word = data[i][0]
                if not word in od:
                    od[word] = []
                od[word].append([name, data[i][1]])

        return od

if __name__ == '__main__':

    DSLFILE = "wordfreq.zz.dsl.test"
    zz = wordfreq()
    zz.printlistinfo()
    od = zz.combineall()
    zz.writedsl(od, DSLFILE)

    print('Total words in final dict: ' + str(len(od)))
    print('Ex: "the" ', od['the'])
    print('Ex: "fabulous" ', od['fabulous'])
    print('Ex: "poignancy" ', od['poignancy'])



