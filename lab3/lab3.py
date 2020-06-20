from StaticHuffmanTree import StaticHuffmanTree
from AdaptiveHuffmanTree import AdaptiveHuffmanTree
import os
import time


def string_from_file(file_path):
    file = open(file_path, encoding='utf-8')

    s = ""
    for line in file:
        s += line.strip("\n")

    file.close()

    return s


def handle_files(files):
    report = open('report.txt', 'w')

    for file in files:
        string = string_from_file(file)

        s_time_start = time.time()
        sht = StaticHuffmanTree(string)
        s_time_end = time.time()
        with open('static.bin', 'wb') as f:
            sht.compressed_text.tofile(f)

        a_time_start = time.time()
        aht = AdaptiveHuffmanTree(string, 27, 97)
        a_time_end = time.time()
        with open('adaptive.bin', 'wb') as f:
            aht.compressed_text.tofile(f)

        ds_time_start = time.time()
        sht.decode()
        ds_time_end = time.time()

        da_time_start = time.time()
        # aht.decode()
        da_time_end = time.time()

        report.write("File size before compressing                                 --- " +
                     str(round(os.stat(file).st_size / 1000, 3)) + "kB\n"
                     "File size after compressing using STATIC Huffman Algorithm   --- " +
                     str(round(os.stat('static.bin').st_size / 1000, 3)) + "kB\n"
                     "File size after compressing using ADAPTIVE Huffman Algorithm --- " +
                     str(round(os.stat('adaptive.bin').st_size / 1000, 3)) + "kB\n"
                     "Compression FACTOR of STATIC Huffman Algorithm   --- " +
                     str(round(os.stat('static.bin').st_size / os.stat(file).st_size * 100, 2)) + "%\n"
                     "Compression FACTOR of ADAPTIVE Huffman Algorithm --- " +
                     str(round(os.stat('adaptive.bin').st_size / os.stat(file).st_size * 100, 2)) + "%\n"
                     "STATIC Huffman Algorithm Compressing time     --- " + str(round(s_time_end - s_time_start, 6)) + "\n"
                     "ADAPTIVE Huffman Algorithm Compressing time   --- " + str(round(a_time_end - a_time_start, 6)) + "\n"
                     "STATIC Huffman Algorithm Decompressing time   --- " + str(round(ds_time_end - ds_time_start, 6)) + "\n"
                     "ADAPTIVE Huffman Algorithm Decompressing time --- " + str(round(da_time_end - da_time_start, 6)) + "\n\n")

        os.remove('static.bin')
        os.remove('adaptive.bin')

    report.close()


if __name__ == "__main__":
    handle_files(["1kB.txt", "10kB.txt", "100kB.txt", "1MB.txt"])
