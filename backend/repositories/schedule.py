from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from utils import get_commits_info

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_executor(ProcessPoolExecutor(1))
    scheduler.add_job(get_commits_info, 'interval', minutes=10)
    scheduler.start()