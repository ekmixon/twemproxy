import os
import re
import sys
import time
import copy
import _thread
import socket
import threading
import logging
import inspect
import argparse
import telnetlib
import redis
import random
import redis
import json
import glob
import subprocess

from collections import defaultdict
from argparse import RawTextHelpFormatter

from string import Template

PWD = os.path.dirname(os.path.realpath(__file__))
WORKDIR = os.path.join(PWD,  '../')

def getenv(key, default):
    return os.environ[key] if key in os.environ else default

logfile = getenv('T_LOGFILE', 'log/t.log')
if logfile == '-':
    logging.basicConfig(level=logging.DEBUG,
        format="%(asctime)-15s [%(threadName)s] [%(levelname)s] %(message)s")
else:
    logging.basicConfig(filename=logfile, level=logging.DEBUG,
        format="%(asctime)-15s [%(threadName)s] [%(levelname)s] %(message)s")

logging.info("test running")

def strstr(s1, s2):
    return s1.find(s2) != -1

def lets_sleep(SLEEP_TIME = 0.1):
    time.sleep(SLEEP_TIME)

def TT(template, args): #todo: modify all
    return Template(template).substitute(args)

def TTCMD(template, args): #todo: modify all
    '''
    Template for cmd (we will replace all spaces)
    '''
    ret = TT(template, args)
    return re.sub(' +', ' ', ret)

def nothrow(ExceptionToCheck=Exception, logger=None):
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ExceptionToCheck as e:
                if logger:
                    logger.info(e)
                else:
                    print(e)

        return f_retry  # true decorator

    return deco_retry

@nothrow(Exception)
def test_nothrow():
    raise Exception('exception: xx')

def json_encode(j):
    return json.dumps(j, indent=4, cls=MyEncoder)

def json_decode(j):
    if isinstance(j, bytes):
        j = str(j, encoding="utf-8")

    return json.loads(j)

#commands does not work on windows..
def system(cmd, log_fun=logging.info):
    if log_fun: log_fun(cmd)
    return subprocess.getoutput(cmd)

def shorten(s, l=80):
    return s if len(s)<=l else f'{s[:l-3]}...'

def assert_true(a):
    assert a, f'assert fail: except true, got {a}'

def assert_equal(a, b):
    assert a == b, f'assert fail: {shorten(str(a))} vs {shorten(str(b))}'

def assert_raises(exception_cls, callable, *args, **kwargs):
    try:
        callable(*args, **kwargs)
    except exception_cls as e:
        return e
    except Exception as e:
        assert False, f'assert_raises {exception_cls} but raised: {e}'
    assert False, f'assert_raises {exception_cls} but nothing raise'

def assert_fail(err_response, callable, *args, **kwargs):
    try:
        callable(*args, **kwargs)
    except Exception as e:
        assert re.search(err_response, str(e)), \
               'assert "%s" but got "%s"' % (err_response, e)
        return

    assert False, f'assert_fail {err_response} but nothing raise'

if __name__ == "__main__":
    test_nothrow()
