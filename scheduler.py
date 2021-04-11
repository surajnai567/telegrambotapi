from apscheduler.schedulers.blocking import BlockingScheduler
import threading
from main import sch


def start():
    sch.start()


message_sending_thread = threading.Thread(target=start)
message_sending_thread.start()