import random
import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOW = -10**9
HIGH = 10**9

def machine_output(a):
    cnt = 0
    for i in range(1, len(a) - 1):
        if a[i] > a[i - 1] and a[i] > a[i + 1]:
            cnt += 1
    return cnt

def build_large(n):
    # Three sections: wide random values, a narrow range full of repeats,
    # and a strict up-down zigzag that finishes on a high value.
    random.seed(20260105)
    values = [random.randint(LOW, HIGH) for _ in range(40000)]
    values += [random.randint(1, 3) for _ in range(30000)]
    rest = n - len(values)
    values += [HIGH if i % 2 == 1 else LOW for i in range(rest)]
    return values

testcases = []

# Smallest inputs
testcases.append([42])                                   # N = 1
testcases.append([3, 8])                                 # N = 2, second value larger

# No value stands above both of its neighbours
testcases.append([2, 4, 6, 8, 10, 12])                   # strictly increasing
testcases.append([9, 7, 5, 3, 1])                        # strictly decreasing
testcases.append([6, 6, 6, 6, 6, 6])                     # all equal

# Single and multiple hits
testcases.append([1, 2, 3, 4, 9, 8, 7, 6, 5])            # one, in the middle of long slopes
testcases.append([1, 5, 2, 6, 3, 7, 1])                  # three, including positions 2 and N-1
testcases.append([HIGH, LOW, 999999999, -5, 0, LOW, HIGH])   # largest values at both ends, extreme values

# Repeated neighbours
testcases.append([1, 4, 4, 2, 5, 5, 5, 3, 6, 2, 7, 7])   # flat tops must not be counted

# Large case (maximum N)
testcases.append(build_large(100000))

# Generate files
for i, a in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")

    with open(input_path, "w", newline="\n") as f:
        f.write(str(len(a)) + "\n" + " ".join(map(str, a)))

    with open(output_path, "w", newline="\n") as f:
        f.write(str(machine_output(a)))

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
