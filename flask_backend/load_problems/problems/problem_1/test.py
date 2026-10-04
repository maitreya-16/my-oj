import random
import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOW = -10**9
HIGH = 10**9

def longest_rising(a):
    best = 1
    cur = 1
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            cur += 1
        else:
            cur = 1
        if cur > best:
            best = cur
    return best

def build_large_mixed(n):
    # Many rising runs of different lengths; the longest one sits in the middle.
    # Every 5th run starts on the same value the previous run ended on.
    random.seed(20260101)
    lengths = []
    total = 0
    while total < 30000:
        length = random.randint(1, 3000)
        lengths.append(length)
        total += length
    lengths.append(31415)
    total += 31415
    while total < n:
        length = min(random.randint(1, 3000), n - total)
        lengths.append(length)
        total += length

    values = []
    last = 0
    for idx, length in enumerate(lengths):
        limit = min(last, HIGH - 100 * length)
        if idx % 5 == 4:
            start = limit
        else:
            start = random.randint(LOW, limit)
        value = start
        for _ in range(length):
            values.append(value)
            value += random.randint(1, 100)
        last = values[-1]
    return values

testcases = []

# Small cases
testcases.append([42])                                   # minimum N
testcases.append([1, 2, 3, 2, 4, 5, 6, 1])               # general case
testcases.append([5, 4, 3, 2, 1])                        # strictly decreasing

# Equal values must break a rising portion
testcases.append([7, 7, 7, 7, 7, 7])                     # all equal
testcases.append([1, 2, 2, 3, 4, 4, 5, 6, 7])            # plateaus inside a non-decreasing sequence

# Value range and position cases
testcases.append([LOW, -999999999, 0, 999999999, HIGH, LOW, HIGH])  # extreme values, negative numbers
testcases.append([9, 8, 7, 1, 2, 3, 4, 5, 6, 7])         # longest portion is at the very end
testcases.append([1, 5, 2, 6, 3, 7, 4, 8, 5, 9])         # must be continuous, not a subsequence

# Large cases (near constraint)
testcases.append(build_large_mixed(100000))                             # many runs, longest in the middle
testcases.append([LOW + 20000 * i for i in range(99999)] + [HIGH])      # maximum N, fully rising

# Generate files
for i, a in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")

    with open(input_path, "w", newline="\n") as f:
        f.write(str(len(a)) + "\n" + " ".join(map(str, a)))

    with open(output_path, "w", newline="\n") as f:
        f.write(str(longest_rising(a)))

# Verify solution.cpp against the generated files
def verify():
    source = os.path.join(BASE_DIR, "solution.cpp")
    compiler = shutil.which("g++")
    if compiler is None:
        print("g++ not found: test files generated, solution.cpp check skipped")
        return 0
    if not os.path.exists(source):
        print("solution.cpp not found")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, "solution.exe" if os.name == "nt" else "solution")
        build = subprocess.run([compiler, "-O2", "-std=c++17", "-o", exe, source],
                               capture_output=True, text=True)
        if build.returncode != 0:
            print("Compilation failed")
            print(build.stderr)
            return 1

        passed = 0
        total = len(testcases)
        for i in range(1, total + 1):
            with open(os.path.join(BASE_DIR, f"input{i}.txt")) as f:
                data = f.read()
            with open(os.path.join(BASE_DIR, f"output{i}.txt")) as f:
                expected = f.read()
            try:
                run = subprocess.run([exe], input=data, capture_output=True, text=True, timeout=10)
                ok = run.returncode == 0 and run.stdout.split() == expected.split()
            except subprocess.TimeoutExpired:
                ok = False
            if ok:
                passed += 1
            print(f"Test {i}: {'PASSED' if ok else 'FAILED'}")

    print(f"{passed}/{total} test cases passed")
    return 0 if passed == total else 1

sys.exit(verify())
