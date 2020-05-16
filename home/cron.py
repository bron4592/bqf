from django_cron import CronJobBase, Schedule
from home.watcher import hotRSI, querys, inHot
from structures.breakout import remove, multiValid, breakout

class validateJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5min
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.valid_job'    # a unique code
    def do(self):
        multiValid()
        remove()
        pass

class structureJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5min
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.struct_job'    # a unique code

    def do(self):
        breakout()
        pass

class rsiJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 1min
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.rsi_job'    # a unique code

    def do(self):
        querys()
        hotRSI()
        inHot()
        pass