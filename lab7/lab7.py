NO_OF_CHARS = 4


def match(text, pattern):
    matches = search(text, pattern)
    print(matches)

    unique_matches = set()
    for m in matches:
        if text[m[0]:m[1] + 1] not in unique_matches:
            unique_matches.add(text[m[0]:m[1] + 1])

    return list(unique_matches)


def search(text, pattern):
    if '*' in pattern or '+' in pattern or '?' in pattern:
        matches = []
        special_characters = []
        new_patterns = []

        fi = 0  # first index not yet in new_patterns
        for i, c in enumerate(pattern):
            if c == '*' or c == '+' or c == '?':
                new_patterns.append(pattern[fi:i-1])
                fi = i + 1
                special_characters.append((pattern[i-1], c))
            if i == len(pattern) - 1:
                new_patterns.append(pattern[fi:])

        new_patterns = [(p, match_dot(text, p)) if '' != p else (p, []) for p in new_patterns]
        print(special_characters)
        print(new_patterns)

        fnep = 0  # first not empty pattern
        lnep = len(new_patterns) - 1  # last non empty pattern
        while fnep < len(new_patterns) and len(new_patterns[fnep][1]) == 0:
            fnep += 1
        while lnep >= 0 and len(new_patterns[lnep][1]) == 0:
            lnep -= 1
        # print("fnep = {}, lnep = {}\n".format(fnep, lnep))

        if lnep == -1:
            end_possibilities = possibilities_at_end(text, special_characters)
            print(end_possibilities)

            for ep in end_possibilities:
                for i in range(len(text)):
                    if ep == text[i:i + len(ep)]:
                        matches.append((i, i + len(ep) - 1))

            return matches

        for fpmi in new_patterns[fnep][1]:  # fpmi - first pattern match index
            # print("fpmi = {}, sci = {}".format(fpmi, sci))

            # find all possibilities before fnep
            curr_matches = []
            possibilities = []
            cur_gac_idx = 1
            inside = False
            plus = False
            for i in range(fnep - 1, -1, -1):
                # print("i = {}, scp = {}".format(i, special_characters[i][0]))
                if special_characters[i][1] == '+':
                    plus = True

                scp = special_characters[i][0]  # special character pattern
                if special_characters[i][1] == '*' or special_characters[i][1] == '?':
                    if len(possibilities) == 0 and not plus:
                        possibilities.append('')

                gac = 1  # good arguments count
                while True:
                    if gac == 2 and special_characters[i][1] == '?':
                        break

                    # print(fpmi, cur_gac_idx, len(scp), text[fpmi - cur_gac_idx:fpmi - cur_gac_idx + len(scp)], scp)
                    if text[fpmi - cur_gac_idx:fpmi - cur_gac_idx + len(scp)] == scp:
                        cur_gac_idx += len(scp)
                        gac += 1
                        # print("Adding {}".format(possibilities[len(possibilities) - 1] + scp))
                        if len(possibilities) == 0:
                            possibilities.append(scp)
                        else:
                            possibilities.append(scp + possibilities[len(possibilities) - 1])
                    else:
                        break
            # print(possibilities)

            paths = [[fpmi]]
            prev_pattern = fnep
            for p in new_patterns[fnep + 1:]:
                if p[0] == '':
                    continue

                new_paths = []
                for i, path in enumerate(paths):
                    for j in p[1]:
                        # print(len(new_patterns[prev_pattern][0]), path[len(path) - 1], j)
                        if j >= path[len(path) - 1] + len(new_patterns[prev_pattern][0]):
                            new_path = path.copy()
                            new_path.append(j)
                            new_paths.append(new_path)
                paths = new_paths
                prev_pattern += 1
            # print(paths)

            for i, path in enumerate(paths):
                # print("Doing path --- {} --- ".format(path))
                prev_pattern = fnep
                curr_pattern = fnep + 1
                curr_path_step = 0

                for p in new_patterns[fnep + 1:]:
                    if p[0] == '':
                        curr_pattern += 1
                        continue

                    inside = True
                    new_text = text[path[curr_path_step] + len(new_patterns[prev_pattern][0]):path[curr_path_step + 1]]
                    new_sp = special_characters[prev_pattern:curr_pattern]
                    # print("Check between {} {} patterns, outcome - {}, elif {} {} {}".format(prev_pattern, curr_pattern, possibilities_between_patterns(new_text, new_sp), curr_pattern, lnep, curr_pattern == lnep))
                    if not possibilities_between_patterns(new_text, new_sp):
                        break
                    elif curr_pattern == lnep:
                        end_possibilities = possibilities_at_end(text[path[len(path) - 1] + 1:], special_characters[lnep:])
                        for ep in end_possibilities:
                            tmp = path.copy()
                            tmp[len(tmp) - 1] = tmp[len(tmp) - 1] + len(ep)
                            curr_matches.append(tmp)
                        # curr_matches.append(path)
                    prev_pattern = curr_pattern
                    curr_pattern += 1
                    curr_path_step += 1

            if not inside:
                end_possibilities = possibilities_at_end(text[fpmi:], special_characters[lnep:])
                # print("NOT INSIDE", fpmi, end_possibilities)
                for ep in end_possibilities:
                    curr_matches.append((fpmi, fpmi + len(ep)))
                # curr_matches = [[fpmi, fpmi]]

            # print(possibilities, curr_matches)
            for pos in possibilities:
                matches += [(m[0] - len(pos), m[len(m) - 1]) for m in curr_matches]

            if fnep == 0:
                matches += curr_matches

        # print("matches - {}".format(matches))
        # return [(m[0], m[len(m) - 1]) for m in matches]
        return matches
    elif '.' in pattern:
        return [(m, m + len(pattern) - 1) for m in match_dot(text, pattern)]
    else:
        return [(m, m + len(pattern) - 1) for m in fa(text, pattern)]


def possibilities_between_patterns(text, special_characters):
    curr = 0
    for i, sp in enumerate(special_characters):
        if sp[1] == '+' and text[curr:curr + len(sp[0])] == sp[0]:
            curr += len(sp[0])
        elif sp[1] == '+':
            return False

        if i + 1 < len(special_characters) and sp[0] == special_characters[i + 1][0] and special_characters[i + 1][1] != '?':
            continue

        if sp[1] == '?':
            if text[curr:curr + len(sp[0])] == sp[0]:
                curr += len(sp[0])
            continue

        while text[curr:curr + len(sp[0])] == sp[0]:
            curr += len(sp[0])

    return curr == len(text)


def possibilities_at_end(text, special_characters):
    # print(text, special_characters, end=' ')
    possibilities = []
    curr = 0
    for sp in special_characters:
        # print(sp, end=' ')
        if (sp[1] == '*' or sp[1] == '?') and len(possibilities) == 0 and curr == 0:
            possibilities.append('')

        gac = 0
        while True:
            if gac >= 1 and sp[1] == '?':
                break

            if text[curr:curr + len(sp[0])] == sp[0]:
                if len(possibilities) == 0:
                    possibilities.append(sp[0])
                else:
                    possibilities.append(possibilities[len(possibilities) - 1] + sp[0])
                curr += len(sp[0])
                gac += 1
            elif sp[1] == '+':
                possibilities = [p for p in possibilities if p != '' and p[len(p) - len(sp[0])] == sp[0]]
                break
            else:
                break
        # print(possibilities)

    return possibilities


def match_dot(text, pattern):
    matches = []
    patterns = pattern.split('.')

    first_non_dot = 0
    for i, p in enumerate(patterns):
        if p == '':
            first_non_dot += 1
        else:
            break

    if first_non_dot == len(patterns):
        return [i for i in range(len(text)) if len(text) - len(pattern) + 1 > i > len(pattern) - 2]

    pms = fa(text, patterns[first_non_dot])  # pms - possible matches

    for pm in pms:  # possible match
        cur_idx = pm + len(patterns[first_non_dot])
        for i, p in enumerate(patterns[first_non_dot + 1:]):
            cur_idx += 1
            if p == '' and i + 1 + first_non_dot == len(patterns) - 1 and cur_idx <= len(text) and pm >= first_non_dot:
                matches.append(pm - first_non_dot)

            if p == '':
                continue

            if text[cur_idx:cur_idx + len(p)] != p:
                break

            if text[cur_idx:cur_idx + len(p)] == p and i + 1 == len(patterns) - 1 and pm >= first_non_dot:
                matches.append(pm - first_non_dot)
                break

    if len(patterns[first_non_dot + 1:]) == 0:
        matches = pms

    return matches


def fa(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []
    tf = compute_trans_fun(pattern)
    # print(str(tf))

    j = 0
    for i in range(n):
        j = tf[j][get_ord(text[i])]
        if j == m:
            matches.append(i - m + 1)

    return matches


def compute_trans_fun(pattern):
    tf = []
    lps = 0
    for i in range(len(pattern)):
        if i == 0:
            tf.append([0] * get_ord(pattern[0]) + [1] + [0] * (NO_OF_CHARS - 1 - get_ord(pattern[0])))
        else:
            tf.append(tf[lps].copy())
            tf[i][get_ord(pattern[i])] = i + 1
        lps = tf[lps][get_ord(pattern[i])] if i != 0 else 0
    tf.append(tf[lps].copy())

    return tf


def get_ord(char):
    return ord(char) - 97


if __name__ == "__main__":
    print("=====================")
    # t = "abbabbab"
    # p = "abba."
    te = "bababbabbbbb"
    #     01234567890
    pa = "ba"
    print(match(te, "b*"))
    # print(possibilities_at_end("bbbbb", [('a', '?'), ('b', '+'), ('a', '+'), ('b', '?')]))
    # print(match(te, pa))
    # print(possibilities_at_end('cbc', [('c', '+'), ('b', '*')]))
