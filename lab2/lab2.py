from Trie import *
from SuffixTree import *
import time


if __name__ == "__main__":
    text_recursive_example_very_long = "abaabbaaabbac"
    text_recursive_example_long = "abaabbaaabbac"
    text_recursive_example_medium = "abaabbaaabbac"
    text_recursive_example_short = "abaabbaaabbac"
    text_recursive_example_very_short = "abaabbaaabbac"

    for i in range(10):
        text_recursive_example_very_long += text_recursive_example_very_long
        text_recursive_example_long += text_recursive_example_long if i < 9 else ""
        text_recursive_example_medium += text_recursive_example_medium if i < 7 else ""
        text_recursive_example_short += text_recursive_example_short if i < 5 else ""
        text_recursive_example_very_short += text_recursive_example_very_short if i < 3 else ""

    short_text = "abaabbaaabbac"

    file = open("1997_714.txt", encoding="utf8")
    file_text = ""

    for line in file:
        file_text += line
    file.close()

    report = open("report.txt", "w")

    report.write("I'm testing these three options (In order: #1 Trie, #2 Suffix Tree using McCreight (with links) "
                 "#3 Suffix Tree without links)\nin six tests with increasing number of characters (exact amount given "
                 "next to examples).\nFirst five examples follow \"abaabbaaabbac\" pattern and the last one is in file "
                 "1997_714.txt.\nThe last example due to usage of a lot of unknown characters will NOT be tested in"
                 "Trie structure and tree without links.\nTime is given in seconds.\n\n\n")

    example_index = 0
    while True:
        if example_index == 0:
            example = short_text
        elif example_index == 1:
            example = text_recursive_example_very_short
        elif example_index == 2:
            example = text_recursive_example_short
        elif example_index == 3:
            example = text_recursive_example_medium
        elif example_index == 4:
            example = text_recursive_example_long
        elif example_index == 5:
            example = text_recursive_example_very_long
        else:
            example = file_text

        # ==================================================================================================================
        report.write("#" + str(example_index + 1) + " example --- Length: " + str(len(example)) + "\n\n")

        if example_index != 6:
            start_time = time.time()
            Trie(example)
            end_time = time.time()
            report.write("Trie      --- {}\n".format(end_time - start_time))

        start_time = time.time()
        SuffixTree(example, 0)
        end_time = time.time()
        report.write("McCreight --- {}\n".format(end_time - start_time))

        if example_index != 6:
            start_time = time.time()
            SuffixTree(example, 1)
            end_time = time.time()
            report.write("No links  --- {}\n".format(end_time - start_time))

        report.write("--- --- --- --- --- --- --- --- ---\n\n")
        # ==================================================================================================================

        example_index += 1

        if example_index == 7:
            break

    report.close()
