ZZ WordFreq
===========

## Current Version

> ver 0.2
> ver 0.1

## Introduction

- 基于网络收集来的词频信息, 进行进一步整理, 选择BNC/ANC/COCA各100k以内的单词, 合并为一单独的dsl词典

- 可用于 [GoldenDict] [Goldendict@github] v1.5

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
> http://www.audiencedialogue.net/bnc.html

- OANC (Open American Naitonal Corpus)

> http://www.anc.org/data/anc-second-release/

- COCA (The Corpus Of Contemporary American English)

> http://corpus.byu.edu/coca/
>
> http://www.pdawiki.com/forum/thread-13667-1-1.html

## Screenshot

![screenshot](https://raw.githubusercontent.com/jjzz/BNC-ANC-word-freqency-list-dsl/master/goldendict_screen.png)

> "[ANC] 6776" 表示在ANC词频中列第6776位

## 注释

- 已移除所有含数字/部分标点符号/全部非ASCII字符的单词

- 仅OANC中将名词单复数 和 动词原型/过去式/过去分词 合并作为同一个单词处理

[goldendict]:http://www.goldendict.org
[goldendict@github]:https://github.com/goldendict/goldendict
