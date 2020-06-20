import math


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

    print("names:     ", end='')
    for k, v in names.items():
        print(k, [e + 1 for e in v[:len(txt)]])

    print("positions: ", end='')
    for k, v in entries.items():
        print(k, [v[e] + 1 for e in range(len(v) - 1)])


def two_dim_pattern(l1, l2, pattern_length=1):
    power = 1
    while power * 2 <= pattern_length:
        power *= 2
    is_power_of_two = True if power == pattern_length else False

    n1, e1 = kmr(l1, power)
    n2, e2 = kmr(l2, power)

    n1 = n1.get(power) if n1.get(power) is not None else []
    n2 = n2.get(power) if n2.get(power) is not None else []
    e1 = e1.get(power)
    e2 = e2.get(power)

    similarities = []

    if is_power_of_two:
        for i in range(min(len(n1), len(n2))):
            pi1 = e1[n1[i]]
            pi2 = e2[n2[i]]
            if l1[pi1:pi1 + power] == l2[pi2:pi2 + power]:
                similarities.append(i)
    else:
        for i in range(min(len(n1), len(n2))):
            if i + pattern_length - power >= len(n1) or i + pattern_length - power >= len(n2):
                continue

            pi1 = e1[n1[i]]
            pi2 = e2[n2[i]]
            pi3 = e1[n1[i + pattern_length - power]]
            pi4 = e2[n2[i + pattern_length - power]]

            if l1[pi1:pi1 + power] == l2[pi2:pi2 + power] and l1[pi3:pi3 + power] == l2[pi4:pi4 + power]:
                similarities.append(i)

    return similarities


def get_similarities_from_lines(lines, length=1):
    all_similarities = []
    for i in range(1, len(lines)):
        lines[i - 1] = lines[i - 1].strip('\n')
        lines[i] = lines[i].strip('\n')

        similarities = two_dim_pattern(lines[i - 1], lines[i], length)
        all_similarities.append((i, similarities))
    return all_similarities


def zad2():
    """
    Solving exercise 2, I assumed I am to look only for letters, hence spaces and newlines are ignored
    :return:
    """
    with open("haystack.txt", "r") as f:
        lines = f.readlines()

    all_similarities = get_similarities_from_lines(lines)

    with open("report.txt", "w") as f:
        f.write("----------------------------------exercise 2----------------------------------------------------------\n"
                "In file haystack.txt finding all situations were the same letter is on the same place on two consequent lines.\n"
                "I assumed I am to look only for letters, hence spaces and newlines are ignored.\n\n"
                "The convention is: first there two lines that were being compared, then in brackets [] there are"
                "\nin order - index of the character and what the character is.\n\n\n")

        for sim in all_similarities:
            f.write("\"{}\"\n\"{}\"\nPatterns --- ".format(lines[sim[0]-1], lines[sim[0]]))

            for match in sim[1]:
                if len(lines[sim[0]]) > match and len(lines[sim[0]-1]) > match and lines[sim[0]][match] != " " and lines[sim[0]][match] != "\n":
                    f.write("[{} \"{}\"], ".format(match, lines[sim[0]][match]))
            f.write("\n\n")
        f.write("----------------------------------end of exercise 2----------------------------------------------------\n")


def zad3():
    with open("haystack.txt", "r") as f:
        lines = f.readlines()

    with open("report.txt", "a+") as f:
        f.write("----------------------------------exercise 3----------------------------------------------------------\n"
                "Searching for \"th\":\n")
        all_similarities = get_similarities_from_lines(lines, 2)

        for sim in all_similarities:
            if len(sim[1]) > 0:
                for match in sim[1]:
                    l1 = lines[sim[0]]
                    l2 = lines[sim[0]-1]
                    if len(l1) > match and len(l2) > match and l1[match:match + 2] == "th":
                        f.write("\"{}\"\n\"{}\"\nMatches --- [{} \"{}\"]\n".format(l1, l2, match, l1[match:match + 2]))

        f.write("\nSearching for \"t h\":\n")
        all_similarities = get_similarities_from_lines(lines, 3)
        for sim in all_similarities:
            if len(sim[1]) > 0:
                for match in sim[1]:
                    l1 = lines[sim[0]]
                    l2 = lines[sim[0] - 1]
                    if len(l1) > match and len(l2) > match and l1[match:match + 3] == "t h":
                        f.write("\"{}\"\n\"{}\"\nMatches --- [{} \"{}\"]\n".format(l1, l2, match, l1[match:match + 3]))

        f.write("----------------------------------end of exercise 3----------------------------------------------------\n")


if __name__ == "__main__":
    zad2()
    zad3()
