# -*- coding: utf-8 -*-
"""
Test main functionality.
"""
import logging
import unittest

from twisted.python import log

from tx_logging import Manager
from tx_logging.tests.observers import CollectingObserver


class LoggingTest(unittest.TestCase):

    def setUp(self):
        self.LOG = Manager().getLogger(__name__)

    def _test_level(self, level, messages_number):
        observer = CollectingObserver(level)
        log.addObserver(observer)

        self.LOG.debug('test debug')
        self.LOG.info('test info')
        self.LOG.warning('test warning')
        self.LOG.error('test error')
        self.LOG.critical('test critical')

        log.removeObserver(observer)
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
