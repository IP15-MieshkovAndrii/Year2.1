from sorter import Sorter
import time

def main():
    sorter = Sorter("a.bin", "b.bin", "c.bin")
    sorter.generate_file(1024**2, 1_000_000)
    sorter.sort()
    print(sorter)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
