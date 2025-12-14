import timeit
from pathlib import Path

# -------- алгоритми пошуку --------

def boyer_moore(text, pattern):
    if not pattern:
        return 0
    last = {}
    for i, ch in enumerate(pattern):
        last[ch] = i
    m = len(pattern)
    n = len(text)
    i = m - 1
    j = m - 1
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            i -= 1
            j -= 1
        else:
            lo = last.get(text[i], -1)
            i += m - min(j, 1 + lo)
            j = m - 1
    return -1

def kmp(text, pattern):
    if not pattern:
        return 0

    def compute_lps(p):
        lps = [0] * len(p)
        length = 0
        i = 1
        while i < len(p):
            if p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    lps = compute_lps(pattern)
    i = j = 0
    n = len(text)
    m = len(pattern)
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp(text, pattern):
    if not pattern:
        return 0
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1
    h = pow(d, m - 1, q)
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t and text[i:i + m] == pattern:
            return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1

# -------- робота з локальними файлами --------

BASE_DIR = Path(r"G:\GOIT\GitHub\goit-algo-hw-05\task3")

file1 = BASE_DIR / "стаття 1.txt"
file2 = BASE_DIR / "стаття 2.txt"   

def read_txt(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()

text1 = read_txt(file1)
text2 = read_txt(file2)

# -------- вимірювання часу --------

def measure_time(alg, text, pattern, number=1000):
    return timeit.timeit(lambda: alg(text, pattern), number=number)

# один реальний і один вигаданий підрядок
pattern_real = "Java"      # змінюй на будь-який точно наявний у тексті
pattern_fake = "abcdef1"    # гарантовано вигаданий

for text, name in [(text1, "стаття 1"), (text2, "стаття 2")]:
    print(f"\nРезультати для {name}:")
    for pattern in (pattern_real, pattern_fake):
        bm = measure_time(boyer_moore, text, pattern)
        kp = measure_time(kmp, text, pattern)
        rk = measure_time(rabin_karp, text, pattern)
        print(f"Підрядок: {pattern!r}")
        print(f"  Боєр-Мур   : {bm:.6f}s")
        print(f"  KMP        : {kp:.6f}s")
        print(f"  Рабін-Карп : {rk:.6f}s")
