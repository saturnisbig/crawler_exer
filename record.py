#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import datetime


class Record:
    def __init__(self, url):
        self.url = url
        self.start_time = datetime.datetime.now()
