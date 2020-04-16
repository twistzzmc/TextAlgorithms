import bitarray as ba
from StaticHuffmanTree import StaticHuffmanTree
from AdaptiveHuffmanTree import AdaptiveHuffmanTree


def string_from_file(file_path):
    file = open(file_path, encoding='utf-8')

    s = ""
    for line in file:
        s += line

    file.close()

    return s


def check_bits(strings):
    report = open("report.txt", "w")

    for string in strings:
        ht = StaticHuffmanTree(string)
        encoding = ht.pseudo_encode(string)

        bits = ba.bitarray()
        bits.frombytes(string.encode('utf-8'))

        report.write("Testing string of size " + str((len(bits) / 8) / 1000) + "kB\n"
                     "Number of bits before compression: " + str(len(bits)) + "\n"
                     "Number of bits after compression:  " + str(len(encoding)) + "\n"
                     "Compression Ratio:                 " +
                     str(round(len(encoding) / len(bits) * 100, 2)) + "%\n\n")

    report.close()


if __name__ == "__main__":
    # s1 = string_from_file("1kB.txt")
    # s2 = string_from_file("1997_714.txt")
    # check_bits([s1, s2])

    # aht = AdaptiveHuffmanTree("aardvark", 26, 97)

    aht = AdaptiveHuffmanTree("aardvark")
    print(aht)
