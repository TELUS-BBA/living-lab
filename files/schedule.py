#!/usr/bin/env python3
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import maya


def intense_test():
    print("Running intense test at {}".format(maya.now().rfc2822()))


def continuous_test():
    print("Running continuous test at {}".format(maya.now().rfc2822()))


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(intense_test, 'cron', hour='*/1', minute=30)
    scheduler.add_job(continuous_test, 'cron', minute='*/5')
    print("Starting scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
