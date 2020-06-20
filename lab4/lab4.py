import numpy as np
from unidecode import unidecode
import spacy
import random
import time


# Ex 3 =====================================================================================
def delta1(a, b):
    if a == b:
        return 0
    else:
        return 1


def delta2(a, b):
    if a == b:
        return 0
    elif unidecode(a) == unidecode(b):
        return 0.5
    else:
        return 1


def edit_distance(x, y, delta):
    edit_table = np.empty((len(x) + 1, len(y) + 1))
    for i in range(len(x) + 1):
        edit_table[i, 0] = i
    for j in range(len(y) + 1):
        edit_table[0, j] = j

    for i in range(len(x)):
        k = i + 1
        for j in range(len(y)):
            p = j + 1
            edit_table[k, p] = min(edit_table[k - 1, p] + 1,
                                   edit_table[k, p - 1] + 1,
                                   edit_table[k - 1, p - 1] + delta(x[i], y[j]))

    return edit_table


def find_operations(x, y, edit_distance_matrix):
    current_cost = edit_distance_matrix[len(x), len(y)]
    current_point = len(x), len(y)
    operation_list = []

    while current_cost > 0:
        direction_cost = min(edit_distance_matrix[current_point[0] - 1, current_point[1] - 1],
                             edit_distance_matrix[current_point[0] - 1, current_point[1]],
                             edit_distance_matrix[current_point[0], current_point[1] - 1])

        if direction_cost == edit_distance_matrix[current_point[0] - 1, current_point[1] - 1]:
            moving_point = current_point[0] - 1, current_point[1] - 1
            direction = 'change'
        elif direction_cost == edit_distance_matrix[current_point[0] - 1, current_point[1]]:
            moving_point = current_point[0] - 1, current_point[1]
            direction = 'delete'
        else:
            moving_point = current_point[0], current_point[1] - 1
            direction = 'insert'

        if edit_distance_matrix[moving_point[0], moving_point[1]] != edit_distance_matrix[current_point[0], current_point[1]]:
            operation_list.append((current_point, direction))
            current_cost -= 1
        current_point = moving_point

    return operation_list


def handle_operations(x, y, operation_list, report):
    o = 0  # relative offset
    for i in range(len(operation_list) - 1, -1, -1):
        k = operation_list[i][0][0] - 1 + o  # absolute position of x character index with offset
        p = operation_list[i][0][1] - 1      # absolute position of y character index
        operation = operation_list[i][1]
        if operation == 'change':
            report.write("{}*{}*{} --- change {} -> {} --- {}".format(x[0:k], y[p], x[k + 1:len(x)], x[k], y[p], x))
            x = x[0:k] + y[p:p + 1] + x[k + 1:len(x)]
            report.write(" -> {}\n".format(x))
        elif operation == 'insert':
            report.write("{}*{}*{} --- insert {} --- {}".format(x[0:k + 1], y[p], x[k + 1:len(x)], y[p], x))
            x = x[0:k + 1] + y[p:p + 1] + x[k + 1:len(x)]
            o += 1
            report.write(" -> {}\n".format(x))
        elif operation == 'delete':
            report.write("{}*{}*{} --- delete {} --- {}".format(x[0:k], x[k], x[k + 1:len(x)], x[k], x))
            x = x[0:k] + x[k + 1:len(x)]
            o -= 1
            report.write(" -> {}\n".format(x))
    return x


def transform_words(input_words, output_words, report):
    for i in range(len(input_words)):
        report.write("Transforming \"{}\" into \"{}\"\n".format(input_words[i], output_words[i]))
        edit_distance_matrix = edit_distance(input_words[i], output_words[i], delta1)
        operation_list = find_operations(input_words[i], output_words[i], edit_distance_matrix)
        output_word = handle_operations(input_words[i], output_words[i], operation_list, report)
        if output_words[i] == output_word:
            result = "Word transformed successfully --- " + output_word
        else:
            result = "Word transformed UNSUCCESSFULLY --- " + output_word
        report.write(result + "\n\n")
# Ex 3 =====================================================================================


# Ex 9 =====================================================================================
def lcs(x, y):
    m = len(x)
    n = len(y)

    L = np.empty((m + 1, n + 1))

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i, j] = 0
            elif x[i - 1] == y[j - 1]:
                L[i, j] = L[i - 1, j - 1] + 1
            else:
                L[i, j] = max(L[i - 1, j], L[i, j - 1])

    print("Longest LCS found! Length - " + str(L[m, n]))
    return L


def lcs_for_tokens(doc1, doc2):
    m = len(doc1)
    n = len(doc2)

    L = np.empty((m + 1, n + 1))

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i, j] = 0
            elif doc1[i - 1].text == doc2[j - 1].text:
                L[i, j] = L[i - 1, j - 1] + 1
            else:
                L[i, j] = max(L[i - 1, j], L[i, j - 1])

    return L


def backtrack_lcs(x, y, L):
    k = len(x)
    p = len(y)
    common_substring = ""

    while k > 0 and p > 0:
        if x[k - 1] == y[p - 1]:
            common_substring += x[k - 1]
            k -= 1
            p -= 1
        else:
            if L[k - 1, p] > L[k, p - 1]:
                k -= 1
            else:
                p -= 1

    return common_substring[::-1]


def backtrack_lcs_for_tokens(doc1, doc2, L):
    k = len(doc1)
    p = len(doc2)
    common_substring = []

    while k > 0 and p > 0:
        if doc1[k - 1].text == doc2[p - 1].text:
            common_substring.append(doc1[k - 1])
            k -= 1
            p -= 1
        else:
            if L[k - 1, p] > L[k, p - 1]:
                k -= 1
            else:
                p -= 1

    return common_substring[::-1]


def get_random_indexes(indexes_count, top_number, bottom_number=0):
    indexes = set()
    for i in range(indexes_count):
        index_found = False
        while not index_found:
            index = random.randint(bottom_number, top_number)
            if index not in indexes:
                indexes.add(index)
                index_found = True

    return indexes


def get_file(file_path):
    file = ""
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        file += line
    f.close()
    return file


def delete_random_tokens_from_file(file_path, percent, file_name=""):
    nlp = spacy.load("en_core_web_sm")
    doc1 = nlp(get_file(file_path))
    tokens_to_delete = len(doc1) - int(((100 - percent) / 100) * len(doc1))
    indexes_set = get_random_indexes(tokens_to_delete, len(doc1))

    f = open(file_name + "_with_removed_tokens.txt", "w", encoding="utf-8")
    for i in range(len(doc1)):
        if i not in indexes_set or doc1[i].text == "\n":
            f.write(doc1[i].text + doc1[i].whitespace_)
    f.close()

    doc2 = nlp(get_file(file_name + "_with_removed_tokens.txt"))

    return doc1, doc2, file_name + "_with_removed_tokens.txt"


def get_lines_from_file(file_path):
    f = open(file_path, "r", encoding="utf-8")
    lines = []
    for line in f:
        lines.append(line)
    f.close()
    return lines


def check_doc_line(doc, ct, differences_in_line, line_index, file_number):
    cti = 0
    for j in range(len(doc)):
        if cti >= len(ct) or ct[cti].text != doc[j].text:
            differences_in_line.append((line_index, doc[j], file_number))
        else:
            cti += 1
    return differences_in_line


def diff(file1_path, file2_path):
    file1 = get_lines_from_file(file1_path)
    file2 = get_lines_from_file(file2_path)

    m = len(file1), 1 if len(file1) < len(file2) else len(file2), 2  # smaller of the two files

    for i in range(len(file1)):
        file1[i] = file1[i].strip("\n")
    for i in range(len(file2)):
        file2[i] = file2[i].strip("\n")

    nlp = spacy.load("en_core_web_sm")

    different_lines = []
    for i in range(m[0]):
        doc1 = nlp(file1[i]) if i < len(file1) else []
        doc2 = nlp(file2[i]) if i < len(file2) else []

        L = lcs_for_tokens(doc1, doc2)
        ct = backtrack_lcs_for_tokens(doc1, doc2, L)  # common tokens

        differences_in_line = []
        differences_in_line = check_doc_line(doc1, ct, differences_in_line, i, 1)
        differences_in_line = check_doc_line(doc2, ct, differences_in_line, i, 2)

        if len(differences_in_line) != 0:
            different_lines.append(differences_in_line)

    return different_lines


def check_diff(file_path, file_name, percent, report):
    doc1, doc2, new_file_path = delete_random_tokens_from_file(file_path, percent, file_name)
    different_lines = diff(file_path, new_file_path)

    report.write("In the difference showcase below first we have line number, then we have listed all differences \n"
                 "in this line in syntax - symbol to which file the difference belongs then the difference in parentheses\n"
                 "e.g. <\"Jan\" means \"Jan\" is not in LCS and is in file number one (< > - first/second file)\n\n")

    report.write("Testing diff function for \"{}\" file\n".format(file_name + ".txt"))

    for different_line in different_lines:
        line_number = different_line[0][0] + 1
        differences = ""

        for difference in different_line:
            differences += "<" if difference[2] == 1 else ">"
            differences += "\"" + difference[1].text + "\" "

        report.write("Line {} --- {}\n".format(line_number, differences))
# Ex 9 =====================================================================================


if __name__ == '__main__':
    rep = open("report.txt", "w+", encoding="utf-8")

    rep.write("========================================================================================================"
              "\nExercise 3\n\n\n")
    input_words_list = ["los", "Łódź", "kwintesencja", "ATGAATCTTACCGCCTCG "]
    output_words_list = ["kloc", "Lodz", "quintessence", "ATGAGGCTCTGGCCCCTG"]
    transform_words(input_words_list, output_words_list, rep)
    rep.write("========================================================================================================"
              "\n\n")

    rep.write("========================================================================================================"
              "\nExercise 9\n\n\nFirst I checked a small sample from the attached text.\n\n")
    check_diff("test.txt", "test", 3, rep)

    rep.write("\n\n\nNow I am checking the whole text\n\n\n")

    time_start = time.time()
    check_diff("romeo-i-julia.txt", "romeo-i-julia", 3, rep)
    time_end = time.time()

    rep.write("========================================================================================================"
              "\n\n")

    rep.close()

    print(time_end - time_start)
