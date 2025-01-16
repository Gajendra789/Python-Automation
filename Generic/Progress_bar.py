## Method 1

import time
import sys

def progress_bar(iterable, total, prefix="", length=40):
    for i, item in enumerate(iterable):
        percent = ("{0:.1f}").format(100 * (i + 1) / float(total))
        filled_length = int(length * (i + 1) // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        # Print progress bar on a new line
        sys.stdout.write(f'{prefix} |{bar}| {percent}% Complete\n')
        sys.stdout.flush()
        yield item
        time.sleep(0.1)

items = range(100)
for item in progress_bar(items, total=len(items), prefix="Progress"):
    pass


## Method 2

import time
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def progress_bar(iterable, total, prefix="", length=40):
    for i, item in enumerate(iterable):
        percent = ("{0:.1f}").format(100 * (i + 1) / float(total))
        filled_length = int(length * (i + 1) // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        logging.info(f'{prefix} |{bar}| {percent}% Complete')
        yield item
        time.sleep(0.1)

items = range(100)
for item in progress_bar(items, total=len(items), prefix="Progress"):
    pass


## Method 3

import time
import sys

def progress_bar(iterable, total, prefix="", length=40):
    for i, item in enumerate(iterable):
        percent = ("{0:.1f}").format(100 * (i + 1) / float(total))
        filled_length = int(length * (i + 1) // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% Complete')
        sys.stdout.flush()
        yield item
        time.sleep(0.1)
    sys.stdout.write('\n')

items = range(100)
for item in progress_bar(items, total=len(items), prefix="Progress"):
    pass
