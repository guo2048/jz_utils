from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from jz_utils import logger_factory
from jz_utils.singleton import singleton

logger = logger_factory.get_logger(__name__)


@singleton
class CronTask:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def add_cron_job(self, fn, cron):
        trigger = CronTrigger.from_crontab(cron)
        self.scheduler.add_job(fn, trigger)
        logger.info(f"{fn.__name__} set to {cron}")

    def add_interval_job_sec(self, fn, interval):
        self.scheduler.add_job(fn, "interval", seconds=interval)


if __name__ == "__main__":
    import datetime
    import time

    # CronTask.add_interval_job_sec(lambda: print("hello 2s"), 2)
    CronTask().add_cron_job(lambda: print(f"hello 1m {datetime.datetime.now()}"), "* * * * *")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        CronTask().shutdown()
        print("调度器已关闭")
