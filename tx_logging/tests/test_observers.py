# -*- coding: utf-8 -*-
"""
Test log observers.
"""
import logging
import tx_logging
import re
import os
import tempfile
import unittest

from datetime import datetime

from twisted.python import log
from tx_logging.observers import LevelFileLogObserver


class LevelFileLogObserverTest(unittest.TestCase):

    rx = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})[+-]\d{2}\d{2}\s+([A-Z]+):\[([\w\.]+)\]:\s(.+)'

    def setUp(self):
        self.LOG = tx_logging.getLogger(__name__)
        self.log_path = tempfile.mktemp()
        self.log_file = open(self.log_path, 'w')

    def tearDown(self):
        self.log_file.close()
        os.remove(self.log_path)

    def _test_level(self, level, messages_number):
        observer = LevelFileLogObserver(self.log_file, level)
        log.addObserver(observer)

        self.LOG.debug('test debug')
        self.LOG.info('test info')
        self.LOG.warning('test warning')
        self.LOG.error('test error')
        self.LOG.critical('test critical')

        log.removeObserver(observer)

        with open(self.log_path) as f:
            lines = [line.strip() for line in f.readlines()]

        self.assertEqual(len(lines), messages_number)

        for line in lines:
            m = re.match(self.rx, line)
            self.assertIsNotNone(m)

            time, level_name, system, entry_text = m.groups()

            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            entry_level = logging.getLevelName(level_name)

            self.assertGreaterEqual(entry_level, level)
            self.assertEqual(system, __name__)

            text = "test {0}".format(level_name.lower())
            self.assertEqual(entry_text, text)

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
