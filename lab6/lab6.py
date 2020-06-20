import math
import time
import sys
from pathlib import Path
from suffix_tree import SuffixTree


def kmr(text, p=-1):
    original_length = len(text)
    factor = math.floor(math.log2(len(text))) if p == -1 else min(p, math.floor(math.log2(len(text)))) if len(text) > 0 else 0
    max_length = 2 ** factor
    padding_length = 2 ** (factor + 1) - 1
    text += 'z' * padding_length

    position_to_index, first_entry = sort_rename(list(text))
    names = {1: position_to_index}
    entries = {1: first_entry}

    for i in range(1, factor):
        power = 2 ** (i - 1)
        new_sequence = []

        for j in range(len(text)):
            if j + power < len(names[power]):
                new_sequence.append((names[power][j], names[power][j + power]))
        # print("power:        " + str(power))
        # print("new sequence: " + str(new_sequence))
        # print("names:        " + str(names[power]) + "\n")

        position_to_index, first_entry = sort_rename(new_sequence)
        names[power * 2] = position_to_index
        entries[power * 2] = first_entry

    return names, entries


def sort_rename(sequence):
    last_entry = None
    index = 0
    position_to_index = [None] * len(sequence)
    first_entry = {}

    for entry in sorted([(e, i) for i, e in enumerate(sequence)]):
        if last_entry and last_entry[0] != entry[0]:
            index += 1
            first_entry[index] = entry[1]

        position_to_index[entry[1]] = index
        if last_entry is None:
            first_entry[0] = entry[1]
        last_entry = entry

    return position_to_index, first_entry


def print_names_and_entries(txt, names, entries):
    print("\ntext:      " + txt)

    print("names:     ")
    for k, v in names.items():
        print(k, [e + 1 for e in v[:len(txt)]])

    print("positions: ")
    for k, v in entries.items():
        print(k, [v[e] + 1 for e in range(len(v) - 1)])


def find_all_patterns(text, pattern):
    if len(pattern) > len(text):
        print("ERROR! Pattern cannot be longer than the text!")
        exit(-1)

    pattern_length = len(pattern)
    power = 1
    while power * 2 <= pattern_length:
        power *= 2
    is_power_of_two = True if power == pattern_length else False

    dbf_start_time_ns = time.time_ns()
    dbf_start_time_s = time.time()
    names, entries = kmr(pattern + '&' + text, p=power)
    dbf_end_time_s = time.time()
    dbf_end_time_ns = time.time_ns()

    names = names[power]
    # print("Power --- {}\nNames --- {}\nPositions --- {}".format(power, names, entries), end="\n\n")

    pattern_indexes = []
    for i, pattern_index in enumerate(names):
        if is_power_of_two and pattern_index == names[0] and i != 0:
            pattern_indexes.append(i - pattern_length - 1)
        elif not is_power_of_two and pattern_index == names[0] and names[i + pattern_length - power] == names[pattern_length - power] and i != 0:
            pattern_indexes.append(i - pattern_length - 1)

    print("Places where pattern is:\n", pattern_indexes)

    return pattern_indexes, names, dbf_end_time_ns - dbf_start_time_ns, dbf_end_time_s - dbf_start_time_s
    # with open("report.txt", "a+", encoding="utf-8") as f:
    #     f.write("It took --- {} ns\nIt took --- {} s\n\n".format(dbf_end_time_ns - dbf_start_time_ns, dbf_end_time_s - dbf_start_time_s))


# Knuth-Pratt-Morris algorithm from GeeksForGeeks
def compute_lps_array(pattern, m, lps):
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1


def kmp_string_matching_geeks(text, pattern):
    matches = []
    m = len(pattern)
    n = len(text)

    lps = [0] * m
    j = 0

    compute_lps_array(pattern, m, lps)

    i = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j-1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    return matches


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    text = ""
    for line in lines:
        text += line

    return text


def zad3():
    def measure_dbf(text, pattern, name):
        with open("report.txt", "a+", encoding="utf-8") as report:
            report.write("Measuring time for DBF --- {}\n".format(name))
            pattern_indexes, names, n_sec, sec = find_all_patterns(text, pattern)
            report.write("It took --- {} ns\nIt took --- {} s\n\n".format(n_sec, sec))

    def measure_suffix_tree(text, name):
        with open("report.txt", "a+", encoding="utf-8") as report:
            report.write("Measuring time for Suffix Tree --- {}\n".format(name))
            start_ns = time.time_ns()
            start_s = time.time()
            tree = SuffixTree(text)
            end_ns = time.time_ns()
            end_s = time.time()
            report.write("It took --- {} ns\nIt took --- {} s\n\n".
                         format(end_ns - start_ns, end_s - start_s))

    romeo = read_file("romeo-i-julia-700.txt")
    patt_romeo = "Romeo"

    statute = read_file("1997_714.txt")
    patt_statute = "Art"

    zad6 = read_file("zad6")
    patt_zad6 = "wzorca"

    with open("report.txt", "a+", encoding="utf-8") as report:
        report.write("==============================zad 3==============================\n"
                     "Measuring build time for DBF and Suffix Tree:\n\n\n")

    measure_dbf(romeo, patt_romeo, "romeo")
    measure_suffix_tree(romeo, "romeo")

    measure_dbf(statute, patt_statute, "statute")
    measure_suffix_tree(statute, "statute")

    measure_dbf(zad6, patt_zad6, "zad6")
    measure_suffix_tree(zad6, "zad6")


def zad4():
    def measure_size(text, pattern, name, path):
        with open("report.txt", "a+", encoding="utf-8") as report:
            report.write("Measuring size for --- {}\n".format(name))
            pattern_indexes, names, n_sec, sec = find_all_patterns(text, pattern)
            report.write("Size of DBF in bytes --- {}\n".format(sys.getsizeof(names)))
            report.write("Size of romeo-i-julia-700.txt in bytes --- {}\n\n".format(Path(path).stat().st_size))

    with open("report.txt", "a+", encoding="utf-8") as report:
        report.write("==============================zad 4==============================\n"
                     "Measuring size of DBF and original text file\n\n\n")

    romeo = read_file("romeo-i-julia-700.txt")
    patt_romeo = "Romeo"

    statute = read_file("1997_714.txt")
    patt_statute = "Art"

    zad6 = read_file("zad6")
    patt_zad6 = "wzorca"

    measure_size(romeo, patt_romeo, "Romeo", "romeo-i-julia-700.txt")
    measure_size(statute, patt_statute, "statute", "1997_714.txt")
    measure_size(zad6, patt_zad6, "zad6", "zad6")


def zad5():
    def measure_finding(text, pattern, name):
        with open("report.txt", "a+", encoding="utf-8") as report:
            kmp_ns_start = time.time_ns()
            kmp_s_start = time.time()
            matches = kmp_string_matching_geeks(text, pattern)
            kmp_s_end = time.time()
            kmp_ns_end = time.time_ns()

            dbf_ns_start = time.time_ns()
            dbf_s_start = time.time()
            pattern_indexes, names, n_sec, sec = find_all_patterns(text, pattern)
            dbf_s_end = time.time()
            dbf_ns_end = time.time_ns()

            report.write("Measuring pattern matches finding time for KMP Algorithm --- {}\n"
                         "It took --- {} ns\nIt took --- {} s\n\n"
                         "Measuring pattern matches finding time for DBF --- {}\n"
                         "It took --- {} ns\nIt took --- {} s\n\n"
                         "Matches indexes for KMP and DBF respectively --- {} for pattern \"{}\":\n{}\n{}\n\n".
                         format(name, kmp_ns_end - kmp_ns_start, kmp_s_end - kmp_s_start,
                                name, dbf_ns_end - dbf_ns_start, dbf_s_end - dbf_s_start,
                                name, pattern, matches, pattern_indexes))

    romeo = read_file("romeo-i-julia-700.txt")
    patt_romeo = "Romeo"

    statute = read_file("1997_714.txt")
    patt_statute = "dnia"

    zad6 = read_file("zad6")
    patt_zad6 = "wzorca"

    with open("report.txt", "a+", encoding="utf-8") as report:
        report.write("==============================zad 5==============================\n"
                     "Comparing matching patterns indexes times for KMP and DBF:\n\n\n")

    measure_finding(romeo, patt_romeo, "Romeo")
    measure_finding(statute, patt_statute, "Statute")
    measure_finding(zad6, patt_zad6, "zad6")


if __name__ == "__main__":
    print("==Start==")

    zad3()
    zad4()
    zad5()
