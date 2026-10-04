import random
import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ascii_sum(s):
    return sum(ord(c) for c in s)

def build_random_printable(n):
    # Random printable ASCII (codes 32-126), many spaces inside,
    # first and last characters are never spaces.
    random.seed(20260104)
    chars = [chr(c) for c in range(33, 127)]
    values = []
    for i in range(n):
        if 0 < i < n - 1 and random.random() < 0.15:
            values.append(" ")
        else:
            values.append(random.choice(chars))
    return "".join(values)

testcases = []

# Small / minimum cases
testcases.append("A")                                    # minimum length, single character
testcases.append("ABC")                                  # uppercase only
testcases.append("hello")                                # lowercase only
testcases.append("A1!")                                  # letter + digit + special
testcases.append("Aa")                                   # same letter, different case
testcases.append("123")                                  # digits only

# Spaces and special characters (reading must not stop at a space)
testcases.append("Hello, World! 2026 :)")                # spaces inside, punctuation
testcases.append("!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~")     # special characters only

# Large cases (maximum length)
testcases.append("~" * 100000)                           # maximum N, maximum possible sum
testcases.append(build_random_printable(100000))         # maximum N, random printable text

# Generate files
for i, s in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")

    with open(input_path, "w", newline="\n") as f:
        f.write(s)

    with open(output_path, "w", newline="\n") as f:
        f.write(str(ascii_sum(s)))

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
