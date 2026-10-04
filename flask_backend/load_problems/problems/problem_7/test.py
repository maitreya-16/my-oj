import random
import os
import shutil
import string
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def transform(word):
    if len(word) <= 10:
        return word
    return word[0] + str(len(word) - 2) + word[-1]

def random_word(length):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

random.seed(20260102)

testcases = []

# Small cases
testcases.append(["word", "localization", "internationalization",
                  "pneumonoultramicroscopicsilicovolcanoconiosis"])     # general case
testcases.append(["a"])                                                 # minimum N, minimum length
testcases.append(["algorithm", "strawberry", "programming", "abbreviation"])  # lengths 9, 10, 11, 12

# Words that must stay unchanged / must all change
testcases.append(["cat", "tree", "house", "planet", "journey", "notebook"])   # all short
testcases.append(["zzzzzzzzzz", "aaaaaaaaaaa", "abababababab", "racecarracecar",
                  "mississippiriver"])                                  # repeated letters, same first and last

# Length boundaries
testcases.append(["x" + "q" * 98 + "y"])                                # single word of maximum length
testcases.append([random_word(length) for length in (1, 2, 10, 11, 12, 99, 100)])  # 1, 2 and 3 character results

# Duplicates
testcases.append(["encyclopedia", "sun", "encyclopedia", "sun", "characteristic",
                  "moon", "characteristic", "abcdefghij", "abcdefghijk", "abcdefghij"])

# Large cases (near constraint)
testcases.append([random_word(random.randint(1, 100)) for _ in range(100)])   # maximum N, mixed lengths
testcases.append([random_word(100) for _ in range(100)])                # maximum N, maximum length

# Generate files
for i, words in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")

    with open(input_path, "w", newline="\n") as f:
        f.write(str(len(words)) + "\n" + "\n".join(words))

    with open(output_path, "w", newline="\n") as f:
        f.write("\n".join(transform(word) for word in words))

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
