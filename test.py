import apscheduler
import threading

from apscheduler.schedulers.blocking import BlockingScheduler

def t(num):
    n = num
    print(n)

print(dir(apscheduler.schedulers.blocking))
l = [1, 2]
sch = BlockingScheduler()
jobs = []
task = threading.Thread(target=sch.start)
task.start()

a = sch.add_job(t, args=[l[0]], trigger='interval', seconds=2)
b = sch.add_job(t,args=[l[1]],trigger='interval', seconds=2)
jobs.append(a)
jobs.append(b)
import time
jobs[1].reschedule(trigger='interval', seconds=2)
for jk in jobs:
    print(jk.next_run_time)
time.sleep(4)
jobs[0].remove()
del l[0]
del jobs[0]
print(jobs)
#print(help(a))