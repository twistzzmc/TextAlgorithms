import re
import string
import time


# Naive algorithm from lecture
def naive_string_matching(text, pattern):
    matches = []
    for s in range(0, len(text) - len(pattern) + 1):
        if pattern == text[s:s+len(pattern)]:
            # print(f"Przesunięcie {s} jest poprawne")
            matches.append(s)
    return matches


# Finite automate algorithm form lecture
def transition_table(pattern):
    alpha = string.ascii_lowercase
    result = []
    for q in range(0, len(pattern) + 1):
        result.append({})
        for a in alpha:
            k = min(len(pattern) + 1, q + 2)
            while True:
                k = k - 1
                if re.search(f"{pattern[:k]}$", pattern[:q] + a):
                    break
            result[q][a] = k
    return result


def fa_string_matching(text, pattern):
    matches = []
    delta = transition_table(pattern)
    q = 0
    for s in range(0, len(text)):
        if text[s] not in delta[q]:
            q = 0
        else:
            q = delta[q][text[s]]
        if q == len(delta) - 1:
            # print(f"Przesunięcie {s + 1 - q} jest poprawne")
            matches.append(s + 1 - q)
    return matches


# Knuth-Pratt_Morris algorithm from lecture
def kmp_string_matching(text, pattern):
    matches = []
    pi = prefix_function(pattern)
    q = 0
    for i in range(0, len(text)):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q-1]
        if pattern[q] == text[i]:
            q = q + 1
        if q == len(pattern):
            # print(f"Przesunięcie {i + 1 - q} jest poprawne")
            matches.append(i + 1 - q)
            q = pi[q-1]
    return matches


def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k-1]
        if pattern[k] == pattern[q]:
            k = k + 1
        pi.append(k)
    return pi


# Naive algorithm from GeeksForGeeks
def naive_string_matching_geeks(text, pattern):
    matches = []
    m = len(pattern)
    n = len(text)

    for i in range(n - m + 1):
        j = 0

        while j < m:
            if text[i + j] != pattern[j]:
                break
            j += 1

        if j == m:
            matches.append(i)

    return matches


# Finite automate algorithm from GeeksForGeeks
NO_OF_CHARS = 256


def fa_string_matching_geeks(text, pattern):
    matches = []

    global NO_OF_CHARS
    m = len(pattern)
    n = len(text)
    tf = compute_transfer_function(pattern, m)

    state = 0
    for i in range(n):
        if ord(text[i]) >= NO_OF_CHARS:
            state = 0
        else:
            state = tf[state][ord(text[i])]
        if state == m:
            matches.append(i - m + 1)

    return matches


def compute_transfer_function(pattern, m):
    global NO_OF_CHARS
    tf = [[0 for i in range(NO_OF_CHARS)] for _ in range(m+1)]

    for state in range(m+1):
        for x in range(NO_OF_CHARS):
            z = get_next_state(pattern, m, state, x)
            tf[state][x] = z

    return tf


def get_next_state(pattern, m, state, x):
    if state < m and x == ord(pattern[state]):
        return state + 1

    i = 0

    for ns in range(state, 0, -1):
        if ord(pattern[ns - 1]) == x:
            while i < ns - 1:
                if pattern[i] != pattern[state - ns + 1 + i]:
                    break
                i += 1
            if i == ns - 1:
                return ns
    return 0


# Knuth-Pratt-Morris algorithm from GeeksForGeeks
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


if __name__ == '__main__':
    ex6 = False
    ex7 = False

    pat = "art"
    times = []
    repetitions = 0

    article = ""
    file = open("1997_714.txt", encoding="utf-8")
    for line in file:
        article += line
    file.close()

    for i in range(repetitions):
        start = time.time()
        naive_string_matching(article, pat)
        end = time.time()
        times.append((end - start, "naive_lecture"))

        start = time.time()
        fa_string_matching(article, pat)
        end = time.time()
        times.append((end - start, "fa_lecture"))

        start = time.time()
        kmp_string_matching(article, pat)
        end = time.time()
        times.append((end - start, "kmp_lecture"))

        start = time.time()
        naive_string_matching_geeks(article, pat)
        end = time.time()
        times.append((end - start, "naive_geeks"))

        start = time.time()
        fa_string_matching_geeks(article, pat)
        end = time.time()
        times.append((end - start, "fa_geeks"))

        start = time.time()
        kmp_string_matching_geeks(article, pat)
        end = time.time()
        times.append((end - start, "kmp_geeks"))

    if repetitions > 0:
        times_sum = [0] * 6
        for time in times:
            if time[1] == "naive_lecture":
                times_sum[0] += time[0]
            elif time[1] == "fa_lecture":
                times_sum[1] += time[0]
            elif time[1] == "kmp_lecture":
                times_sum[2] += time[0]
            elif time[1] == "naive_geeks":
                times_sum[3] += time[0]
            elif time[1] == "fa_geeks":
                times_sum[4] += time[0]
            elif time[1] == "kmp_geeks":
                times_sum[5] += time[0]

        print(f"Naive algorithm from lecture time:              {times_sum[0]}, average time: {times_sum[0] / repetitions}")
        print(f"Finite automate algorithm from lecture time:    {times_sum[1]}, average time: {times_sum[1] / repetitions}")
        print(f"Knuth-Pratt-Morris algorithm from lecture time: {times_sum[2]}, average time: {times_sum[2] / repetitions}")

        print(f"Naive algorithm from geeks time:                {times_sum[3]}, average time: {times_sum[3] / repetitions}")
        print(f"Finite automate algorithm from geeks time:      {times_sum[4]}, average time: {times_sum[4] / repetitions}")
        print(f"Knuth-Pratt-Morris algorithm from geeks time:   {times_sum[5]}, average time: {times_sum[5] / repetitions}")

    # Naive two times slower (ex 6)
    if ex6:
        txt = "aaaaaaaaaaaaaaaab"
        for i in range(21):
            txt += txt
        pat = "aaab"

        print(len(txt), len(pat))

        time1 = time.time()
        naive_string_matching(txt, pat)
        time2 = time.time()
        fa_string_matching(txt, pat)
        time3 = time.time()
        kmp_string_matching(txt, pat)
        time4 = time.time()
        naive_string_matching_geeks(txt, pat)
        time5 = time.time()
        fa_string_matching_geeks(txt, pat)
        time6 = time.time()
        kmp_string_matching_geeks(txt, pat)
        time7 = time.time()

        print(f"Naive lecture:              {time2 - time1}")
        print(f"Finite automate lecture:    {time3 - time2}")
        print(f"Knuth-Pratt-Morris lecture: {time4 - time3}")

        print(f"Naive geeks:                {time5 - time4}")
        print(f"Finite automate geeks:      {time6 - time5}")
        print(f"Knuth-Pratt-Morris geeks:   {time7 - time6}")

    # Transition table two times slower (ex 7)
    if ex7:
        pat = "aaaaaaaaaaaaaaa"
        for i in range(5):
            pat += pat

        time1 = time.time()
        transition_table(pat)
        time2 = time.time()
        prefix_function(pat)
        time3 = time.time()

        print(f"Transition table time: {time2 - time1}")
        print(f"Prefix function time:  {time3 - time2}")

    # Finding Kruszwil
    file = open("tokens-with-entities.tsv", encoding="utf-8")
    wikipedia = ""
    for line in file:
        wikipedia += line

    kruszwil_start = time.time()
    matches = fa_string_matching(wikipedia, "Kruszwil")
    kruszwil_end = time.time()

    print(f"Using finite automate algorithm from lecture it took {kruszwil_end - kruszwil_start} to find the Kruszwil!")
