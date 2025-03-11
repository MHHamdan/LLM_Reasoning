#threading : Process an instance of a program (e.g a Python interpreter)
#process is interuptable or killable, seperate memory, Great for CPU, started independently
#Threads: starting a process is slower than starting a thread, More memory, IPC (inter-process communication) more complicated
#thread: An entity within a process that can be scheduled on(leightweight) is created A process can spawn multiple threads
#threads share the same memory, leightweight, starting a thread is faster, I/O-bound tasks are more

#race conditions
# GIL global interpreter lock,
#A lock that allows only one thread at a time to execute in Python
#Needed in cPython since memory management is not thread safe, avoid multiprocess, free-thread safe, wrapper (C/C++) scipy, numpy, etc


from multiprocessing import Process
import os


# def square_numbers():
#     for i in range(1000):
#         result = i * i
#
#
# if __name__ == "__main__":
#     processes = []
#     num_processes = os.cpu_count()
#
#     # create processes and asign a function for each process
#     for i in range(num_processes):
#         process = Process(target=square_numbers)
#         processes.append(process)
#
#     # start all processes
#     for process in processes:
#         process.start()
#
#     # wait for all processes to finish
#     # block the main thread until these processes are finished
#     for process in processes:
#         process.join()


from threading import Thread, Lock, current_thread
import os
import time

database_vale = 0

def sequar_numbers():
    for i in range(100):
        r = i * i
        time.sleep(0.2)

# if __name__ == '__main__':
#     threads = []
#     num_threads = 10 #os.cpu_count()
#
#     for i in range(num_threads):
#         t = Thread(target=sequar_numbers)
#         threads.append(t)
#
#     #start
#     for t in threads:
#         t.start()
#
#     #join
#     for t in threads:
#         t.join()
#
#     print('end main')
#



def increase1(lock):
    global database_vale

    lock.acquire()
    local_compy = database_vale

    #processing
    local_compy +=1
    time.sleep(0.1)
    database_vale = local_compy
    lock.release()
    
def increase(lock):
    global database_vale

    with lock:
        local_compy = database_vale

        #processing
        local_compy +=1
        time.sleep(0.1)
        database_vale = local_compy

    
# if __name__ == '__main__':
#     lock = Lock()
#
#     print('start value', database_vale)
#     thread1 = Thread(target=increase, args=(lock,))
#     thread2 = Thread(target=increase, args=(lock,))
#     thread3 = Thread(target=increase, args=(lock,))
#
#
#     thread1.start()
#     thread2.start()
#     thread3.start()
#
#     thread1.join()
#     thread2.join()
#     thread3.join()
#
#
#     print('end value ', database_vale)
#     print('end main')

print('queue ... linear data stucture that follows a FIFO queue: first in first serve, first in first out')

from queue import Queue




def worder(q, lock):
    while True:
        value = q.get()
        with lock:
         print(f"in {current_thread().name} got {value}")
        q.task_done()
if __name__ == '__main__':
    q = Queue()
    lock = Lock()
    # q.put(1)
    # q.put(2)
    # q.put(3)
    #
    # #Enter oure    3 2 1 >>>
    #
    # first = q.get()
    # print(first)
    #
    # q.task_done()
    #
    # q.join() # blocks until all item in the queue is processed.



    num_threads = 10

    for i in range(num_threads):
        thread = Thread(target=worder, args=(q, lock))
        thread.daemon = True
        thread.start()


    for i in range(1, 21):
        q.put(i)

    q.join() # blocks until all

    print('end main')



