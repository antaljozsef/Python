import multiprocessing


# Egy mellékfolyamat, ami adatokat ír a Queue-ba
def writer(queue):
    data = 10
    queue.put(data)


# Egy mellékfolyamat, ami olvas az Queue-ból
def reader(queue):
    data = queue.get()
    print(data)


if __name__ == "__main":
    # Hozzunk létre egy Queue-t
    queue = multiprocessing.Queue()

    # Indítsuk a mellékfolyamatokat
    writer_process = multiprocessing.Process(target=writer, args=(queue,))
    reader_process = multiprocessing.Process(target=reader, args=(queue,))

    writer_process.start()
    reader_process.start()

    # Várjuk meg, hogy a writer_process befejezze a munkát
    writer_process.join()

    # Mielőtt befejeznénk a reader_process-t, helyezzünk egy None értéket a Queue-ba, hogy jelezze a befejezést
    queue.put(None)
    reader_process.join()

    print("Fő folyamat befejezve.")
