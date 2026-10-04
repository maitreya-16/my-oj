import random
import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONSONANTS = "bcdfghjklmnpqrstvwxyz"   # includes 'y', which is not a vowel here

def count_vowels(s):
    return sum(1 for c in s if c in "aeiou")

def build_random_mixed(n):
    random.seed(20260102)
    letters = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(letters) for _ in range(n))

testcases = []

# Small / minimum cases
testcases.append("a")                                    # minimum length, a vowel
testcases.append("z")                                    # minimum length, no vowel

# General cases
testcases.append("hello")                                # repeated consonants
testcases.append("programming")                          # vowels spread out
testcases.append("aeiou")                                # all five vowels
testcases.append("rhythm")                               # no vowels, contains 'y'
testcases.append("education")                            # many vowels, mixed order

# Boundary cases (maximum length)
testcases.append("aeiou" * 20)                           # length 100, every letter a vowel
testcases.append((CONSONANTS * 5)[:100])                 # length 100, no vowels (includes 'y')
testcases.append(build_random_mixed(100))                # length 100, random letters

# Generate files
for i, s in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")

    with open(input_path, "w", newline="\n") as f:
        f.write(s)

    with open(output_path, "w", newline="\n") as f:
        f.write(str(count_vowels(s)))

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
