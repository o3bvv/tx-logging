# -*- coding: utf-8 -*-
"""
Test lof observers.
"""
import logging

from twisted.python import log


class CollectingObserver(object):

    def __init__(self, level=logging.INFO):
        self.log = []
        self.log_level = level

    def __call__(self, eventDict):
        if eventDict['isError']:
            level = logging.ERROR
        elif 'level' in eventDict:
            level = eventDict['level']
        else:
            level = logging.INFO
        if level < self.log_level:
            return

        text = log.textFromEventDict(eventDict)
        if text is None:
            return

        self.log.append({
            'level': level,
            'text': text,
            'system': eventDict['system'],
        })
