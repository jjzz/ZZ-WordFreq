ZZ WordFreq
===========

## Current Version

- WordFreq 更新至 v0.3

  原来的 BNC 数据来自 Adam Kilgarriff, 现标记为`BNC.AK`

  本次新增来自 Paul Nation 的 BNC 数据, 标记为`BNC.PN`,
  其特点是将所有单词按 family 组织, 按词频每 1000 个 word families 一个大组, 共 14 组, 14000 个最常用 word family, 实际含单词(包括各种单复数形式等)近50000.
  比如, society/societal/societies 的词频数都是 1000, 表示此 family 属最常见的1000个 word families.

  btw: "BNC Top-15000" 的版本来源不明, 目前已弃用

## Introduction

- 基于网络上现成的 BNC/ANC/COCA 等词频信息, 合并为dsl词典

- 可用于 [GoldenDict] [Goldendict@github] v1.5+

ZZ WordFreq
> top 100k from BNC/ANC/COCA
- wordfreq.zz.dsl
- wordfreq.zz.ann

ZZ's BNC Top-15000 Word List (En)
> word & frequency only
- bnc15000.ann
- bnc15000.dsl

ZZ's BNC Top-15000 Word List (En-Cn)
> word & frequency & very simple Chinese translation
- bnc15000cn.ann
- bnc15000cn.dsl

## Reference

- BNC (British National Corpus)

> http://www.natcorp.ox.ac.uk
>
> http://www.kilgarriff.co.uk/bnc-readme.html
>
> http://www.victoria.ac.nz/lals/about/staff/paul-nation
>
> http://www.audiencedialogue.net/bnc.html

- OANC (Open American Naitonal Corpus)

> http://www.anc.org/data/anc-second-release/

- COCA (The Corpus Of Contemporary American English)

> http://corpus.byu.edu/coca/
>
> http://www.pdawiki.com/forum/thread-13667-1-1.html

## Screenshot

![screenshot](https://raw.githubusercontent.com/jjzz/BNC-ANC-word-freqency-list-dsl/master/screen01.png)

![screenshot](https://raw.githubusercontent.com/jjzz/BNC-ANC-word-freqency-list-dsl/master/screen02.png)

> "[ANC] 6776" 表示在ANC词频中列第6776位

## 注释

- 已移除所有含数字/部分标点符号/全部非ASCII字符的单词

- OANC 中将名词单复数 和 动词原型/过去式/过去分词 合并作为同一个单词处理


[goldendict]:http://www.goldendict.org
[goldendict@github]:https://github.com/goldendict/goldendict
