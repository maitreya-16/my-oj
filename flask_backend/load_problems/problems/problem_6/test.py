"""
Test generator and validator for this problem.

    python test.py              validate the existing files (creates any that are missing)
    python test.py --generate   rewrite input1..10 / output1..10 from scratch, then validate

Checks performed:
    1. every input file obeys the constraints
    2. every output file equals the reference answer computed here in Python
    3. description.json is valid, has the expected fields, and its samples are correct
    4. solution.cpp compiles and reproduces every output file and every sample

Exit status is 0 only when everything passes.
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MAX_LEN = 100000
JSON_KEYS = ["title", "description", "score", "input_format", "output_format", "constraints",
             "isjunior", "time_limit", "memory_limit", "event_id", "samples"]

def lock_answer(code):
    result = []
    i = 0
    while i < len(code):
        j = i
        while j < len(code) and code[j] == code[i]:
            j += 1
        result.append(str(j - i))
        result.append(code[i])
        i = j
    return "".join(result)

def is_valid_input(code):
    return re.fullmatch(r"[0-9]{1,%d}" % MAX_LEN, code) is not None

def different_digit(previous):
    digit = random.choice("0123456789")
    while digit == previous:
        digit = random.choice("0123456789")
    return digit

def build_no_repeats(length):
    digits = []
    previous = ""
    for _ in range(length):
        previous = different_digit(previous)
        digits.append(previous)
    return "".join(digits)

def build_mixed_runs(length):
    # Blocks of every size: mostly short, some with 2-digit and 3-digit sizes, one with a 4-digit size.
    sizes = [1234]
    total = 1234
    while total < length:
        kind = random.random()
        if kind < 0.70:
            size = random.randint(1, 9)
        elif kind < 0.95:
            size = random.randint(10, 99)
        else:
            size = random.randint(100, 400)
        size = min(size, length - total)
        sizes.append(size)
        total += size
    random.shuffle(sizes)
    parts = []
    previous = ""
    for size in sizes:
        previous = different_digit(previous)
        parts.append(previous * size)
    return "".join(parts)

random.seed(20260104)

testcases = []

# Small cases
testcases.append("0")                        # minimum length, the digit 0
testcases.append("3322251")                  # general case
testcases.append("1234567890")               # every digit different from its neighbour

# Cases that separate the intended rule from similar-looking ones
testcases.append("1221121")                  # the same digit appears in several separate blocks
testcases.append("000120003")                # code starting with zeros

# Block-size boundaries
testcases.append("9" * 9 + "8" * 10 + "7" * 11)   # sizes 9, 10 and 11
testcases.append("1" * 100)                  # one block of 100

# Large cases (near constraint)
testcases.append("9" * MAX_LEN)              # maximum length, a single block
testcases.append(build_no_repeats(MAX_LEN))  # maximum length, longest possible answer
testcases.append(build_mixed_runs(MAX_LEN))  # maximum length, blocks of every size

# Generate files
force = "--generate" in sys.argv
for i, code in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")
    if not force and os.path.exists(input_path) and os.path.exists(output_path):
        continue

    with open(input_path, "w", newline="\n") as f:
        f.write(code)

    with open(output_path, "w", newline="\n") as f:
        f.write(lock_answer(code))

# Validate
def read(name):
    with open(os.path.join(BASE_DIR, name), encoding="utf-8") as f:
        return f.read()

def compile_solution(tmp):
    source = os.path.join(BASE_DIR, "solution.cpp")
    compiler = shutil.which("g++")
    if compiler is None:
        print("g++ not found: solution.cpp check skipped")
        return None, True
    if not os.path.exists(source):
        print("solution.cpp not found")
        return None, False
    exe = os.path.join(tmp, "solution.exe" if os.name == "nt" else "solution")
    build = subprocess.run([compiler, "-O2", "-std=c++17", "-o", exe, source],
                           capture_output=True, text=True)
    if build.returncode != 0:
        print("Compilation failed")
        print(build.stderr)
        return None, False
    return exe, True

def solution_agrees(exe, data, expected):
    if exe is None:
        return True
    try:
        run = subprocess.run([exe], input=data, capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return False
    return run.returncode == 0 and run.stdout.split() == expected.split()

def validate():
    all_ok = True
    with tempfile.TemporaryDirectory() as tmp:
        exe, compiled = compile_solution(tmp)
        all_ok = all_ok and compiled

        # input/output files
        passed = 0
        total = len(testcases)
        for i in range(1, total + 1):
            data = read(f"input{i}.txt")
            expected = read(f"output{i}.txt")
            problems = []
            if not is_valid_input(data):
                problems.append("input breaks the constraints")
            elif lock_answer(data) != expected.strip():
                problems.append("output file does not match the reference answer")
            if not solution_agrees(exe, data, expected):
                problems.append("solution.cpp gives a different output")
            if problems:
                print(f"Test {i}: FAILED ({'; '.join(problems)})")
            else:
                passed += 1
                print(f"Test {i}: PASSED")
        print(f"{passed}/{total} test cases passed")
        all_ok = all_ok and passed == total

        # description.json
        try:
            description = json.loads(read("description.json"))
        except (OSError, ValueError) as error:
            print(f"description.json: FAILED ({error})")
            return 1
        if list(description.keys()) != JSON_KEYS:
            print("description.json: FAILED (fields differ from the expected schema)")
            all_ok = False
        samples = description.get("samples", [])
        good = 0
        for j, sample in enumerate(samples, start=1):
            data = sample.get("input", "")
            expected = sample.get("output", "")
            problems = []
            if not is_valid_input(data):
                problems.append("input breaks the constraints")
            elif lock_answer(data) != expected:
                problems.append("output does not match the reference answer")
            if not solution_agrees(exe, data, expected):
                problems.append("solution.cpp gives a different output")
            if problems:
                print(f"Sample {j}: FAILED ({'; '.join(problems)})")
            else:
                good += 1
                print(f"Sample {j}: PASSED")
        print(f"{good}/{len(samples)} samples in description.json passed")
        all_ok = all_ok and len(samples) > 0 and good == len(samples)

    print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
    return 0 if all_ok else 1

sys.exit(validate())
