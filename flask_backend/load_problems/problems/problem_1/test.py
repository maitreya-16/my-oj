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
    return max(a) - min(a)

random.seed(20260106)

testcases = []

# Smallest inputs
testcases.append([-7])                                   # N = 1
testcases.append([12, 5])                                # N = 2, larger value first

# Simple shapes
testcases.append([2, 4, 6, 8, 10, 12])                   # already in increasing order
testcases.append([6, 6, 6, 6, 6, 6])                     # all equal

# Sign cases
testcases.append([-3, -15, -8, -1, -9])                  # all negative
testcases.append([50, 20, 90, 10, 70, 40])               # all positive, extremes in the middle
testcases.append([0, -5, 5, -5, 5, 0, 3])                # mixed signs, extremes repeated

# Value boundaries
testcases.append([HIGH, LOW, 0])                         # largest possible answer

# Large cases (maximum N)
testcases.append([random.randint(LOW, HIGH) for _ in range(100000)])        # full value range
testcases.append([random.randint(100000, 100500) for _ in range(100000)])   # narrow positive range

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
