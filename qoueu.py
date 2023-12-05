import multiprocessing


def writer():
    a = 1
    print(a)


def reader():
    b = 2
    print(b)


if __name__ == "__main__":
    # Indítsuk a mellékfolyamatokat
    writer_process = multiprocessing.Process(target=writer)
    reader_process = multiprocessing.Process(target=reader)

    writer_process.start()
    reader_process.start()

    writer_process.join()
    reader_process.join()

    print("Fő folyamat befejezve.")
