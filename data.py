import multiprocessing
from time import sleep


def writer(q):
    temp = 3
    cnt = 0
    while True:
        cnt = cnt + 1
        if cnt == 10:
            break
        print("Data put into queue.")
        q.put(cnt)
        sleep(0.5)


# Egy mellékfolyamat, ami olvas a Queue-ból
def reader(q):
    cnt = 0
    while True:
        cnt = cnt + 1
        if cnt == 10:
            break
        item = q.get()
        print(f"Received: {item}")


q = multiprocessing.Queue()

print("Main")

writer_process = multiprocessing.Process(target=writer, args=(q,))
reader_process = multiprocessing.Process(target=reader, args=(q,))

writer_process.start()
reader_process.start()

writer_process.join()
reader_process.join()
