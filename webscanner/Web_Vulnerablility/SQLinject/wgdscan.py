#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Web_Vulnerablility.SQLinject.lib.core.Spider import SpiderMain


def main(url):
    root = url
    threadNum = 10
    ret = []
    # spider
    wgd = SpiderMain(root, threadNum)
    ret = wgd.craw()
    # print(ret)
    return ret

