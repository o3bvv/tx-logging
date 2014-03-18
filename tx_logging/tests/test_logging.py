# -*- coding: utf-8 -*-
"""
Test main functionality.
"""
import logging
import unittest

from twisted.python import log as tx_log
from tx_logging import Manager


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

        text = tx_log.textFromEventDict(eventDict)
        if text is None:
            return

        self.log.append({
            'level': level,
            'text': text,
            'system': eventDict['system'],
        })


class LoggingTest(unittest.TestCase):

    def setUp(self):
        self.LOG = Manager().get_logger(__name__)

    def _test_level(self, level, messages_number):
        observer = CollectingObserver(level)
        tx_log.addObserver(observer)

        self.LOG.debug('test debug')
        self.LOG.info('test info')
        self.LOG.warning('test warning')
        self.LOG.error('test error')
        self.LOG.critical('test critical')

        tx_log.removeObserver(observer)
        self.assertEqual(len(observer.log), messages_number)

        for entry in observer.log:
            self.assertGreaterEqual(entry['level'], level)
            text = "test {0}".format(
                    logging.getLevelName(entry['level']).lower())
            self.assertEqual(entry['text'], text)
            self.assertEqual(entry['system'], __name__)

    def test_level_noset(self):
        self._test_level(logging.NOTSET, 5)

    def test_level_debug(self):
        self._test_level(logging.DEBUG, 5)

    def test_level_info(self):
        self._test_level(logging.INFO, 4)

    def test_level_warning(self):
        self._test_level(logging.WARNING, 3)

    def test_level_error(self):
        self._test_level(logging.ERROR, 2)

    def test_level_critical(self):
        self._test_level(logging.CRITICAL, 1)
