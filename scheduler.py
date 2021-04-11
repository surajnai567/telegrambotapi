from apscheduler.schedulers.blocking import BlockingScheduler
import threading
sch = BlockingScheduler()
message_sending_thread = threading.Thread(target=sch.start())
message_sending_thread.start()