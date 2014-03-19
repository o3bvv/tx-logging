tx-logging
==========

[![Build Status](https://travis-ci.org/oblalex/tx-logging.png)](https://travis-ci.org/oblalex/tx-logging)
[![PyPi package](https://badge.fury.io/py/tx-logging.png)](http://badge.fury.io/py/tx-logging/)
[![Downloads](https://pypip.in/d/tx-logging/badge.png)](https://crate.io/packages/tx-logging/)

This is a tiny Python library which extends Twisted logging facilities.

## Synopsis

Tired to log your messages in the following way?

    log.msg("some message", level=logging.DEBUG, system="foo")

With 'tx-logging' you will be able to log messages in your Twisted applications
in a common pythonic way with support of log name and log levels:

    LOG = tx_logging.getLogger("foo")

    LOG.debug("some message")

## Installation

Simple as this:

    pip install tx-logging

## Configuring

To make things work, you will need to add an observer to Twisted's log. It's
name is `LevelFileLogObserver`. It is based on `FileLogObserver` and it can log
to a file or to stdout.

### To log to stdout:

    import sys
    import logging

    from twisted.python import log
    from tx_logging.observers import LevelFileLogObserver


    observer = LevelFileLogObserver(sys.stdout, logging.INFO)
    log.addObserver(observer)

### To log to a file:

    import logging

    from twisted.python import log
    from twisted.python.logfile import LogFile
    from tx_logging.observers import LevelFileLogObserver


    log_file = LogFile.fromFullPath(
        '/path/to/application.log',
        rotateLength=1024 * 1024 * 10, # 10 MiB
        maxRotatedFiles=10)
    observer = LevelFileLogObserver(log_file, logging.INFO)
    log.addObserver(observer)

### Configuring in `tac` files:

    import logging

    from twisted.application import service
    from twisted.python.log import ILogObserver
    from twisted.python.logfile import LogFile
    from tx_logging.observers import LevelFileLogObserver


    log_file = LogFile.fromFullPath(
        'application.log',
        rotateLength=1024 * 1024 * 10, # 10 MiB
        maxRotatedFiles=10)
    observer = LevelFileLogObserver(log_file, logging.INFO)

    application = service.Application("Application Name")
    application.setComponent(ILogObserver, observer.emit)

### Configuring time format

`FileLogObserver` has a [timeFormat](http://twistedmatrix.com/trac/browser/tags/releases/twisted-13.2.0/twisted/python/log.py#L329) attribute, which is set to `None` by
default and time will be formatted as `%Y-%m-%d %H:%M:%S%z`, e.g.:

    2014-03-19 09:53:11+0200     INFO:[-]: Log opened.

You can set your own format in [strftime](http://docs.python.org/2/library/time.html#time.strftime) notation, e.g.:

    observer.timeFormat = "%Y/%m/%d %H:%M:%S"

Resulting output:

    2014/03/19 09:55:51     INFO:[-]: Log opened.

## Usage

Usage is similar to usage of common Python logging:

    import tx_logging

    LOG = tx_logging.getLogger("some log")

    LOG.debug("test debug")
    LOG.info("test info")
    LOG.warning("test warning")
    LOG.error("test error")
    LOG.critical("test critical")

Simple as it is. Assuming that log level was set to `DEBUG`, this will produce:

    2014-03-19 10:49:58+0200    DEBUG:[some log]: test debug
    2014-03-19 10:49:58+0200     INFO:[some log]: test info
    2014-03-19 10:49:58+0200  WARNING:[some log]: test warning
    2014-03-19 10:49:58+0200    ERROR:[some log]: test error
    2014-03-19 10:49:58+0200 CRITICAL:[some log]: test critical

As you can see, logger name can be set to any string, but you may prefer this:

    LOG = tx_logging.getLogger(__name__)
