import multiprocessing


def writer(q):
    for item in range(5):
        print(f"Writing {item} to the queue")
        q.put(item)


def reader(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Read {item} from the queue")


if __name__ == "__main":
    q = multiprocessing.Queue()

    writer_process = multiprocessing.Process(target=writer, args=(q,))
    reader_process = multiprocessing.Process(target=reader, args=(q,))

    writer_process.start()
    reader_process.start()

    writer_process.join()
    q.put(None)  # Signal the reader process to exit
    reader_process.join()

    print("Fő folyamat befejezve.")
